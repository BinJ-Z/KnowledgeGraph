from pathlib import Path
import pandas as pd
import sys
CODE_DIR = Path("/Users/bohe/Desktop/KnowledgeGraph/code")
sys.path.insert(0, str(CODE_DIR))
from sixxxx import AllEdges



input_dir = Path("/Users/bohe/Desktop/KnowledgeGraph/data/source_3")
output_dir = Path("/Users/bohe/Desktop/KnowledgeGraph/data/output_1")


all_edges=AllEdges (
    input_dir=Path("/Users/bohe/Desktop/KnowledgeGraph/data/source_3"),
    output_dir=Path("/Users/bohe/Desktop/KnowledgeGraph/data/output_1"),
)

