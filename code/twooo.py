import pandas as pd
from pathlib import Path

DATABASE_file= "/Users/bohe/Desktop/KnowledgeGraph/database_normalization/DATABASE.tsv"


def Match(input_file,  paper_normalized_column,):
    

    database = pd.read_csv( DATABASE_file, sep="\t", dtype="string",)

    input_file = input_file.merge(
        database,
        left_on = paper_normalized_column,
        right_on="normalized_name",
        how ="left",
)


    input_file = input_file.rename(
        columns={ "standard_id": paper_normalized_column + "_standard_id" }
    )

    input_file = input_file.drop(
        columns=[
            "name",
            "normalized_name",
            "name_type",
            "category",
    ]
)
    

    return input_file



