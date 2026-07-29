# conda activate gliner
# cd "/Users/bohe/Desktop/KnowledgeGraph/code/TXT extract"
# python RunAll.py

from pathlib import Path
from JsonExtract import ExtractResults
from JsonFormat import json_results_to_txt
from GLiNER import RelEx
from gliner import GLiNER


input_dir = Path("/Users/bohe/Desktop/KnowledgeGraph/data/PMC_Bioc")
Extract_dir = Path("/Users/bohe/Desktop/KnowledgeGraph/data/PMC_Extract_result")
format_dir= ( "/Users/bohe/Desktop/KnowledgeGraph/data/PMC_format_result_txt")
output_file = "/Users/bohe/Desktop/KnowledgeGraph/data/source_3/all_relations.xlsx"

ExtractResults(
    input_dir=input_dir,
    output_dir=Extract_dir,
)


json_results_to_txt(
    input_dir=Extract_dir ,
    output_dir=format_dir,
)


relations = RelEx(
    input_dir=format_dir,
    output_file=output_file,
    entity_threshold=0.5,
    relation_threshold=0.5,
)

