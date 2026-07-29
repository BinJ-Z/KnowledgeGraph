#NCBI Taxonomy FTP: https://ftp.ncbi.nlm.nih.gov/pub/taxonomy/new_taxdump/
#NCBI GENE FTP: https://www.ncbi.nlm.nih.gov/gene/------Download/FTP-----https://ftp.ncbi.nih.gov/gene/------ DATA/GENE_INFO/Mammalia/Homo_sapiens.gene_info.gz
#NCBI GENE FTP: https://ftp.ncbi.nih.gov/gene/DATA/GENE_INFO/Mammalia/Homo_sapiens.gene_info.gz
#MONDO disease ontology: ttps://github.com/monarch-initiative/mondo/releases/latest/download/mondo.obo
#HMDB metabolite ontology: https://hmdb.ca/system/downloads/current/hmdb_metabolites.zip
#Uniprot protein: https://www.uniprot.org/
# (reviewed:true) AND (organism_id:9606 OR organism_id:10090)
#TSV：Entry	Entry Name	Protein names


import pandas as pd
from pathlib import Path
import xml.etree.ElementTree as ET


GENE_dir= Path("/Users/bohe/Desktop/KnowledgeGraph/database/Homo_sapiens.gene_info")
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

gene = pd.read_csv(
    GENE_dir,
    sep="\t",
    usecols=[
        "#tax_id",
        "GeneID",
        "Symbol",
        "Synonyms",
        "Full_name_from_nomenclature_authority"
    ],
    dtype="string"
)


gene = gene.rename(
    columns={
        "#tax_id": "tax_id",
        "GeneID": "gene_id"
    }
)


# Official symbols

Official_name = gene[
    [
        "tax_id",
        "gene_id",
        "Symbol"
    ]
].rename(
    columns={
        "Symbol": "gene_name"
    }
).copy()

Official_name["name_type"] = "symbol"

Official_name["gene_name"] = (
    Official_name["gene_name"]
    .str.strip()
)

Official_name = Official_name[
    Official_name["gene_name"].notna()
    & Official_name["gene_name"].ne("")
    & Official_name["gene_name"].ne("-")
].copy()


Official_name["gene_standard_id"] = (
    "NCBIGene:"
    + Official_name["gene_id"]
)




Official_name["gene_normalized_name"] = normalize_name(
    Official_name["gene_name"]
)


Official_name["category"] = "Gene"


Official_name = Official_name.drop_duplicates(
    subset=[
        "gene_standard_id",
        "gene_normalized_name"
    ]
).reset_index(drop=True)


Official_name = Official_name[
    [
        "gene_id",
        "gene_standard_id",
        "gene_name",
        "gene_normalized_name",
        "name_type",
        "category"
    ]
]




# Full names

full_name = gene[
    [
        "tax_id",
        "gene_id",
        "Full_name_from_nomenclature_authority"
    ]
].rename(
    columns={
        "Full_name_from_nomenclature_authority": "gene_name"
    }
).copy()

full_name["name_type"] = "full_name"

full_name["gene_name"] = (
    full_name["gene_name"]
    .str.strip()
)


full_name = full_name[
    full_name["gene_name"].notna()
    & full_name["gene_name"].ne("")
    & full_name["gene_name"].ne("-")
].copy()


full_name["gene_standard_id"] = (
    "NCBIGene:"
    + full_name["gene_id"]
)




full_name["gene_normalized_name"] = normalize_name(
    full_name["gene_name"]
)

full_name["category"] = "Gene"


full_name = full_name.drop_duplicates(
    subset=[
        "gene_standard_id",
        "gene_normalized_name"
    ]
).reset_index(drop=True)


full_name = full_name[
    [
        "gene_id",
        "gene_standard_id",
        "gene_name",
        "gene_normalized_name",
        "name_type",
        "category"
    ]
]




# Synonyms

synonym_name = gene[
    [
        "tax_id",
        "gene_id",
        "Synonyms"
    ]
].rename(
    columns={
        "Synonyms": "gene_name"
    }
).copy()


synonym_name["gene_name"] = (
    synonym_name["gene_name"]
    .str.split("|", regex=False)
)

synonym_name = synonym_name.explode(
    "gene_name",
    ignore_index=True
)

synonym_name["name_type"] = "synonym"

synonym_name["gene_name"] = (
    synonym_name["gene_name"]
    .str.strip()
)


synonym_name = synonym_name[
    synonym_name["gene_name"].notna()
    & synonym_name["gene_name"].ne("")
    & synonym_name["gene_name"].ne("-")
].copy()


synonym_name["gene_standard_id"] = (
    "NCBIGene:"
    + synonym_name["gene_id"]
)



synonym_name["gene_normalized_name"] = normalize_name(
    synonym_name["gene_name"]
)

synonym_name["category"] = "Gene"


synonym_name = synonym_name.drop_duplicates(
    subset=[
        "gene_standard_id",
        "gene_normalized_name"
    ]
).reset_index(drop=True)


synonym_name = synonym_name[
    [
        "gene_id",
        "gene_standard_id",
        "gene_name",
        "gene_normalized_name",
        "name_type",
        "category"
    ]
]



gene_mapping = pd.concat(
    [
        Official_name,
        full_name,
        synonym_name
    ],
    ignore_index=True
)



gene_mapping.to_csv(output_dir / "GENE.tsv", sep="\t", index=False)


