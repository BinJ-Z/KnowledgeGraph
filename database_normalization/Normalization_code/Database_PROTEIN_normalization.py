import pandas as pd
import re
from pathlib import Path
import pronto



UniProt_dir= Path("/Users/bohe/Desktop/KnowledgeGraph/database/UniProt_download.tsv")
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


protein_mapping = pd.read_csv(UniProt_dir, sep="\t", dtype="string")


protein_mapping = protein_mapping.rename(
    columns={
        "Entry": "uniprot_id",
        "Entry Name": "entry_name",
        "Protein names": "protein_name",
        "Organism": "organism"
    }
)


protein_mapping["protein_name"] = (
    protein_mapping["protein_name"]
    .astype("string")
    .str.strip()
)


protein_mapping = protein_mapping[
    protein_mapping["protein_name"].notna()
    & protein_mapping["protein_name"].ne("")
].copy()


protein_mapping["protein_standard_id"] = (
    "UniProtKB:"
    + protein_mapping["uniprot_id"]
)


protein_mapping["protein_normalized_name"] = normalize_name(
    protein_mapping["protein_name"]
)


protein_mapping["name_class"] = "primary"


protein_mapping["category"] = "Protein"


protein_mapping = (
    protein_mapping
    .drop_duplicates(
        subset=[
            "protein_standard_id",
            "protein_normalized_name"
        ]
    )
    .reset_index(drop=True)
)


protein_mapping = protein_mapping[
    [
        "uniprot_id",
        "protein_standard_id",
        "protein_name",
        "protein_normalized_name",
        "name_class",
        "category"
    ]
]


protein_mapping.to_csv(output_dir / "PROTEIN.tsv", sep="\t", index=False)