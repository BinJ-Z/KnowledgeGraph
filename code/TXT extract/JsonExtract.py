from pathlib import Path
import json


def ExtractResults(
    input_dir,
    output_dir,
):

    input_dir = Path(input_dir)
    output_dir = Path(output_dir)

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    for input_file in input_dir.glob("*.json"):

        with open(input_file, encoding="utf-8") as f:
            bioc = json.load(f)

        for collection in bioc:

            for document in collection["documents"]:

                document["passages"] = [
                    passage
                    for passage in document["passages"]
                    if "RESULT" in passage["infons"].get(
                        "section_type",
                        "",
                    ).upper()
                ]

        with open(
            output_dir / input_file.name,
            "w",
            encoding="utf-8",
        ) as f:

            json.dump(
                bioc,
                f,
                ensure_ascii=False,
                indent=2,
            )

    return


