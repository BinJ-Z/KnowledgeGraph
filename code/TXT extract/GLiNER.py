# conda create -n gliner python=3.11 -y
# conda activate gliner
# pip install gliner pandas openpyxl lxml biopython

# conda activate gliner
# cd /Users/bohe/Desktop/pubmed
# python GLiNER.py




from pathlib import Path
import pandas as pd
from gliner import GLiNER


ENTITY_LABELS = [
    "microorganism",
    "metabolite",
    "disease",
    "gene",
    "protein",
]


RELATION_LABELS = [
    "associated_with",
    "affects",
    "increases",
    "decreases",
    "produces",
    "regulates",
    "causes",
    "inhibits",
    "activates",
    "treats",
]


LABEL_MAP = {
    "microorganism": "OrganismTaxon",
    "metabolite": "SmallMolecule",
    "disease": "Disease",
    "gene": "Gene",
    "protein": "Protein",
}


def RelEx(
    input_dir,
    output_file,
    model_name="knowledgator/gliner-relex-base-v1.0",
    entity_threshold=0.8,
    relation_threshold=0.7,
):

    input_dir = Path(input_dir)
    output_file = Path(output_file)
    output_file.parent.mkdir( parents=True, exist_ok=True,)
    model = GLiNER.from_pretrained( model_name)

    all_relations = []

    for input_file in input_dir.glob("*.txt"):

        print(f"Processing: {input_file.name}")

        text = input_file.read_text( encoding="utf-8")

        entities, relations = model.inference(
            [text],
            labels=ENTITY_LABELS,
            relations=RELATION_LABELS,
            threshold=entity_threshold,
            relation_threshold=relation_threshold,
        )

        file_relations = relations[0]

        for relation in file_relations:

            head = relation["head"]
            tail = relation["tail"]

            all_relations.append(
                {
                    "pmc_id": input_file.stem,
                    "subject": head["text"],
                    "subject_type": LABEL_MAP.get(
                        head["type"],
                        head["type"],
                    ),

                    "object": tail["text"],
                    "object_type": LABEL_MAP.get(
                        tail["type"],
                        tail["type"],
                    ),

                    "predicate": relation["relation"],
                    "score": relation["score"],
                    "subject_start": head["start"],
                    "subject_end": head["end"],
                    "object_start": tail["start"],
                    "object_end": tail["end"],
                }
            )

    columns = [
        "pmc_id",
        "subject",
        "subject_type",
        "object",
        "object_type",
        "predicate",
        "score",
        "subject_start",
        "subject_end",
        "object_start",
        "object_end",
    ]

    if all_relations:

        all_relations = pd.DataFrame( all_relations)
        all_relations = all_relations.drop_duplicates(
            subset=[
                "pmc_id",
                "subject",
                "object",
                "predicate",
            ]
        ).reset_index(   drop=True)

    else:

        all_relations = pd.DataFrame( columns=columns)


    all_relations.to_excel( output_file, index=False,)

    print(
        f"\nTotal relations: "
        f"{len(all_relations)}"
    )

    print( f"\nSaved to:\n{output_file}" )

    return all_relations
