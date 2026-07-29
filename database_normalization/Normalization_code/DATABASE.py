import pandas as pd
from pathlib import Path

database_dir=Path("/Users/bohe/Desktop/KnowledgeGraph/database_normalization")
disease = pd.read_csv(database_dir/ "DISEASE.tsv", sep="\t", dtype="string")
gene = pd.read_csv(database_dir/ "GENE.tsv", sep="\t", dtype="string")
protein = pd.read_csv(database_dir/ "PROTEIN.tsv", sep="\t", dtype="string")
taxonomy = pd.read_csv(database_dir/ "TAXDUMP.tsv", sep="\t", dtype="string")
hmdb = pd.read_csv(database_dir/ "HMDB.tsv", sep="\t", dtype="string")



# Disease
disease = disease.rename(
    columns={
        "disease_standard_id": "standard_id",
        "disease_name": "name",
        "disease_normalized_name": "normalized_name",
        "name_class": "name_type",
    }
)

disease = disease[["standard_id", "name", "normalized_name", "name_type", "category"]]


# Gene
gene = gene.rename(
    columns={
        "gene_standard_id": "standard_id",
        "gene_name": "name",
        "gene_normalized_name": "normalized_name",
        "name_type": "name_type",
    }
)

gene = gene[["standard_id", "name", "normalized_name", "name_type", "category"]]


# Protein
protein = protein.rename(
    columns={
        "protein_standard_id": "standard_id",
        "protein_name": "name",
        "protein_normalized_name": "normalized_name",
        "name_class": "name_type",
    }
)

protein = protein[["standard_id", "name", "normalized_name", "name_type", "category"]]


# Taxonomy
taxonomy = taxonomy.rename(
    columns={
        "taxdump_standard_id": "standard_id",
        "name_txt": "name",
        "taxdump_normalized_name": "normalized_name",
        "name_class": "name_type",
    }
)

taxonomy = taxonomy[["standard_id", "name", "normalized_name", "name_type", "category"]]


# HMDB
hmdb = hmdb.rename(
    columns={
        "hmdb_standard_id": "standard_id",
        "hmdb_name": "name",
        "hmdb_normalized_name": "normalized_name",
        "hmdb_name_type": "name_type",
    }
)

hmdb = hmdb[["standard_id", "name", "normalized_name", "name_type", "category"]]

DATABASE = pd.concat(
    [
        disease,
        gene,
        protein,
        taxonomy,
        hmdb,
    ],
    ignore_index=True,
)


DATABASE.to_csv( database_dir / "DATABASE.tsv",  sep="\t", index=False,)