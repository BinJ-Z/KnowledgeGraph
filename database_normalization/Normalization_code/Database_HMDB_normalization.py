#NCBI Taxonomy FTP: https://ftp.ncbi.nlm.nih.gov/pub/taxonomy/new_taxdump/
#NCBI GENE FTP: https://ftp.ncbi.nih.gov/gene/DATA/gene_info.gz
#MONDO disease ontology: ttps://github.com/monarch-initiative/mondo/releases/latest/download/mondo.obo
#HMDB metabolite ontology: https://hmdb.ca/system/downloads/current/hmdb_metabolites.zip
#Uniprot protein: https://www.uniprot.org/
# (reviewed:true) AND (organism_id:9606 OR organism_id:10090)
#TSV：Entry	Entry Name	Protein names

import pandas as pd
from pathlib import Path
import xml.etree.ElementTree as ET



HMDB_dir= Path("/Users/bohe/Desktop/KnowledgeGraph/database/hmdb_metabolites.xml")
output_dir=Path("/Users/bohe/Desktop/KnowledgeGraph/database_normalization")

def normalize_name(series):

    return (
        series
        .astype("string")
        .str.strip()
        .str.replace("’", "'", regex=False)
        .str.replace("′", "'", regex=False)
        .str.replace("–", "-", regex=False)
        .str.replace("—", "-", regex=False)
        .str.replace("−", "-", regex=False)
        .str.replace("_", " ", regex=False)
        .str.replace(r"\s*-\s*", "-", regex=True)
        .str.replace(r"\s+", " ", regex=True)
        .str.lower()
    )

# HMDB XML 

namespace = "{http://www.hmdb.ca}"
records = []

for event, element in ET.iterparse(HMDB_dir, events=("end",)):

    if element.tag != f"{namespace}metabolite":
        continue

    hmdb_id = element.find(f"{namespace}accession").text.strip()
    hmdb_name = element.find(f"{namespace}name").text.strip()

    records.append({
        "hmdb_id": hmdb_id,
        "hmdb_name": hmdb_name,
        "hmdb_name_type": "primary_name"
})
    # Synonyms
    hmdb_synonyms_name = element.find(f"{namespace}synonyms")

    if hmdb_synonyms_name is not None:

        for synonym_element in hmdb_synonyms_name.findall(f"{namespace}synonym"):

            if synonym_element.text is None:
                continue

            synonym = synonym_element.text.strip()

            if not synonym:
                continue

            records.append({
                "hmdb_id": hmdb_id,
                "hmdb_name": synonym,
                "hmdb_name_type": "synonym"
            })

    # Release memory
    element.clear()

HMDB = (pd.DataFrame(records).drop_duplicates())

HMDB["hmdb_standard_id"] = (
    HMDB["hmdb_id"]
    .astype("string")
    .str.strip()
)

HMDB["category"] = "SmallMolecule"



HMDB["hmdb_normalized_name"] = normalize_name(
    HMDB["hmdb_name"]
)

HMDB = HMDB[
    [
        "hmdb_id",
        "hmdb_standard_id",
        "hmdb_name",
        "hmdb_normalized_name",
        "hmdb_name_type",
        "category"
    ]
]

HMDB.to_csv(output_dir/"HMDB.tsv", sep="\t", index=False)

