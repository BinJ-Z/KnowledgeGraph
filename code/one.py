#NormPaperXlsx=normalize_paper_xlsx
#Supplementary information from the paper must be in xlsx format.

import pandas as pd
from pathlib import Path

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

def normalize_paper_xlsx(input_file):

    input_file = Path(input_file)

    paper = pd.read_excel(input_file)

    paper["subject_normalized_name"] = normalize_name(
        paper["subject"]
    )

    paper["object_normalized_name"] = normalize_name(
        paper["object"]
    )

    paper = paper[
        [
            "subject_normalized_name",
            "object_normalized_name",
            "predicate",
        ]
    ].copy()

    return paper
