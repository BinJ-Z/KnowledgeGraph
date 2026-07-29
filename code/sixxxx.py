from pathlib import Path
import pandas as pd
from fiveee import BuildEdgePipeline


def AllEdges(
    input_dir,
    output_dir, 
):

    input_dir = Path(input_dir)
    output_dir = Path(output_dir)

    for input_file in input_dir.rglob("*.xlsx"):

        output_file = output_dir / f"{input_file.stem}_edges.tsv"

        if output_file.exists():
            print(f"Skip: {input_file.name}")
            continue


        BuildEdgePipeline(
            input_file=input_file,
            output_file=output_dir / f"{input_file.stem}_edges.tsv",
        )

    edge_tables = [
        pd.read_csv(edge_file, sep="\t", dtype="string")
        for edge_file in output_dir.rglob("*_edges.tsv")
    ]

    for_edges = pd.concat(
        edge_tables,
        ignore_index=True,
    ).drop_duplicates().reset_index(drop=True)


    all_edges = for_edges[  
    [
        "Subject_ID",
        "Object_ID",
        "predicate",
    ]
    ].copy()

    all_edges = all_edges.rename(
        columns={
            "Subject_ID": ":START_ID",
            "Object_ID": ":END_ID",
            "predicate": ":TYPE",
        }
    )

    all_edges.to_csv(
        output_dir / "all_edges.tsv",
        sep="\t",
        index=False,
    )

    return all_edges