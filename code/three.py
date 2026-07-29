from pathlib import Path
from twooo import Match


def Match_all( input_file,):

    matched_data = Match(
        input_file=input_file,
        paper_normalized_column="subject_normalized_name",
    )

    matched_data = Match(
        input_file=matched_data,
        paper_normalized_column="object_normalized_name",
    )

    return matched_data
