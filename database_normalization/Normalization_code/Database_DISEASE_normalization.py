#NCBI Taxonomy FTP: https://ftp.ncbi.nlm.nih.gov/pub/taxonomy/new_taxdump/
#NCBI GENE FTP: https://ftp.ncbi.nih.gov/gene/DATA/gene_info.gz
#MONDO disease ontology: ttps://github.com/monarch-initiative/mondo/releases/latest/download/mondo.obo
#HMDB metabolite ontology: https://hmdb.ca/system/downloads/current/hmdb_metabolites.zip
#Uniprot protein: https://www.uniprot.org/
# (reviewed:true) AND (organism_id:9606 OR organism_id:10090)
#TSV：Entry	Entry Name	Protein names

import pandas as pd
import re
from pathlib import Path
import pronto



DISEASE_dir= Path("/Users/bohe/Desktop/KnowledgeGraph/database/mondo.obo")
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

ontology = pronto.Ontology(DISEASE_dir)

records = []


for term in ontology.terms():

    disease_id = str(term.id).strip()

    if not disease_id.startswith("MONDO:"):
        continue

    # Remove obsolete MONDO terms

    if term.obsolete:
        continue

    # Primary disease name

    if term.name is not None:

        disease_name = str(term.name).strip()

        if disease_name:

            records.append(
                {
                    "disease_id": disease_id,
                    "disease_name": disease_name,
                    "name_class": "primary"
                }
            )

    # Disease synonyms

    for synonym in term.synonyms:

        synonym_name = str(
            synonym.description
        ).strip()

        if not synonym_name:
            continue

        synonym_scope = str(
            synonym.scope
        ).strip().lower()

        records.append(
            {
                "disease_id": disease_id,
                "disease_name": synonym_name,
                "name_class": synonym_scope
            }
        )



disease_mapping = pd.DataFrame(records)


# Remove missing or empty names

disease_mapping["disease_name"] = (
    disease_mapping["disease_name"]
    .astype("string")
    .str.strip()
)

disease_mapping = disease_mapping[
    disease_mapping["disease_name"].notna()
    & disease_mapping["disease_name"].ne("")
].copy()


# Normalize disease names


disease_mapping["disease_normalized_name"] = normalize_name(
    disease_mapping["disease_name"]
)

# Biolink category

disease_mapping["category"] = "Disease"

disease_mapping["disease_standard_id"] = disease_mapping["disease_id"]

# Remove duplicate mappings

disease_mapping = (
    disease_mapping
    .drop_duplicates(
        subset=[
            "disease_id",
            "disease_normalized_name"
        ]
    )
    .reset_index(drop=True)
)


# Reorder columns

disease_mapping = disease_mapping[
    [
        "disease_id",
        "disease_standard_id",
        "disease_name",
        "disease_normalized_name",
        "name_class",
        "category"
    ]
]



disease_mapping.to_csv(
    output_dir / "DISEASE.tsv",
    sep="\t",
    index=False
)
