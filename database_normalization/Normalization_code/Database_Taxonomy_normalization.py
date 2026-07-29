#NCBI Taxonomy FTP: https://ftp.ncbi.nlm.nih.gov/pub/taxonomy/new_taxdump/
#NCBI GENE FTP: https://ftp.ncbi.nih.gov/gene/DATA/gene_info.gz
#MONDO disease ontology: ttps://github.com/monarch-initiative/mondo/releases/latest/download/mondo.obo
#HMDB metabolite ontology: https://hmdb.ca/system/downloads/current/hmdb_metabolites.zip
#Uniprot protein: https://www.uniprot.org/
# (reviewed:true) AND (organism_id:9606 OR organism_id:10090)
#TSV：Entry	Entry Name	Protein names

import pandas as pd
from pathlib import Path



TAXDUMP_dir=Path("/Users/bohe/Desktop/KnowledgeGraph/database/new_taxdump/names.dmp")
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

taxonomy = pd.read_csv(
    TAXDUMP_dir,
    sep=r"\t\|\t",
    engine="python",
    header=None,
    names=[
        "tax_id",
        "name_txt",
        "unique_name",
        "name_class"
    ],
    dtype=str
)


taxonomy["name_class"] = (
    taxonomy["name_class"]
    .str.replace(r"\t\|$", "", regex=True)
    .str.strip()
)

taxonomy = taxonomy[
    taxonomy["name_class"] != "authority"
].copy()

taxonomy["name_txt"] = (
    taxonomy["name_txt"]
    .astype(str)
    .str.strip()
)

taxonomy["taxdump_normalized_name"] = normalize_name(
    taxonomy["name_txt"]
)


taxonomy["taxdump_standard_id"] = (
    "NCBITaxon:"
    + taxonomy["tax_id"].astype("string")
)

taxonomy["category"] = "OrganismTaxon"

taxonomy = taxonomy[
    [
        "tax_id",
        "taxdump_standard_id",
        "name_txt",
        "taxdump_normalized_name",
        "name_class",
        "category"
    ]
]

taxonomy.to_csv(output_dir/"TAXDUMP.tsv", sep="\t", index=False)

