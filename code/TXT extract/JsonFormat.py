import json
from pathlib import Path


def json_results_to_txt(
    input_dir,
    output_dir,
):

    input_dir = Path(input_dir)
    output_dir = Path(output_dir)

    output_dir.mkdir( parents=True, exist_ok=True, )

    for json_file in input_dir.glob("*.json"):

        with open(
            json_file,
            "r",
            encoding="utf-8",
        ) as file:
            data = json.load(file)

        pmcid = json_file.stem

        if isinstance(data, list):
            collections = data
        else:
            collections = [data]

        results_text = []

        for collection in collections:

            for document in collection.get(
                "documents",
                [],
            ):

                for passage in document.get(
                    "passages",
                    [],
                ):

                    infons = passage.get(
                        "infons",
                        {},
                    )

                    section_type = (
                        infons
                        .get("section_type", "")
                        .strip()
                        .upper()
                    )

                    text = (
                        passage
                        .get("text", "")
                        .strip()
                    )

                    if (
                        section_type == "RESULTS"
                        and text
                    ):

                        # 避免重复写入 Results 标题
                        if text.strip().upper() == "RESULTS":
                            continue

                        results_text.append(text)

        output_file = ( output_dir / f"{pmcid}.txt" )

        output_content = (
            f"{pmcid}\n\n"
            + "\n\n".join(results_text)
)

        with open(
            output_file,
            "w",
            encoding="utf-8",
        ) as file:
            file.write(output_content)

        print(f"Saved: {output_file}")