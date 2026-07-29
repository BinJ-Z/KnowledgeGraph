from one import normalize_paper_xlsx
from three import Match_all
from fourrr import BuildEdge


def BuildEdgePipeline(
    input_file,
    output_file,
):

    Nor = normalize_paper_xlsx( input_file=input_file,)

    Mat = Match_all(
        input_file=Nor,
    )

    Edge = BuildEdge(
        input_file=Mat,
        output_file=output_file,
 )

    return Edge