import pandas as pd
from pathlib import Path

edges_file = Path("/Users/bohe/Desktop/KnowledgeGraph/database_normalization/DATABASE.tsv")
all_nodes_file = Path("/Users/bohe/Desktop/KnowledgeGraph/data/output_1/all_nodes.tsv")

nodes = pd.read_csv(edges_file, sep="\t", dtype="string")

all_nodes = (
    nodes[["standard_id", "normalized_name", "category"]]
    .rename(
        columns={
            "standard_id": "id:ID",
            "normalized_name": "name",
            "category": ":LABEL"
        }
    )
    .drop_duplicates(subset=["id:ID"], keep="first")
    .reset_index(drop=True)
)

all_nodes_file.parent.mkdir(parents=True, exist_ok=True)

all_nodes.to_csv(
    all_nodes_file,
    sep="\t",
    index=False,
)