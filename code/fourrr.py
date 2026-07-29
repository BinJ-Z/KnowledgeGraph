from pathlib import Path


def BuildEdge(
    input_file,
    output_file,
):

    output_file = Path(output_file)

    edges = input_file.copy()

    edges = edges.rename(
    columns={
        "subject_normalized_name": "subject_name",
        "object_normalized_name": "object_name",
        "subject_normalized_name_standard_id": "Subject_ID",
        "object_normalized_name_standard_id": "Object_ID",
    }
)




    edges = edges[
        edges["Subject_ID"].notna()
        & edges["Object_ID"].notna()
    ].copy()


    edges = edges.drop_duplicates().reset_index( drop=True)

    output_file.parent.mkdir( parents=True, exist_ok=True,)



    edges = edges[
    [

        "Subject_ID",
        "subject_name",
        "Object_ID",
        "object_name",
        "predicate",
    ]
].copy()

    edges.to_csv(
        output_file,
        sep="\t",
        index=False,
    )

    return edges



