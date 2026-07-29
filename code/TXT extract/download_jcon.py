from pathlib import Path
from time import sleep
import requests
from Bio import Entrez


Entrez.email = "jenie618@gmail.com"


output_dir = Path("/Users/bohe/Desktop/KnowledgeGraph/data/PMC_BioC")
output_dir.mkdir(parents=True, exist_ok=True)

keywords = (
    '('
    'microbiome*[Title/Abstract] '
    'OR microbiota[Title/Abstract] '
    'OR bacteria*[Title/Abstract] '
    'OR gut*[Title/Abstract] '
    'OR 16S*[Title/Abstract] '
    ') '

    'AND ('
    'omics[Title/Abstract] '
    'OR multi-omics[Title/Abstract] '
    'OR multiomics[Title/Abstract] '
    'OR metabolomics[Title/Abstract] '
    'OR metabolite*[Title/Abstract] '
    'OR proteomics[Title/Abstract] '
    'OR protein*[Title/Abstract] '
    'OR transcriptomics[Title/Abstract] '
    'OR RNA-seq[Title/Abstract] '
    'OR genomics[Title/Abstract] '
    'OR gene*[Title/Abstract] '
    ') '

    'AND Clinical Trial[Publication Type] '
    'NOT Review[Publication Type] '
)


start_year = 2019
end_year = 2025
max_papers = 202


search_query = (
    f"({keywords}) "
    f'AND "{start_year}/01/01"[Publication Date] '
    f': "{end_year}/12/31"[Publication Date] '
    f'AND english[Language] '
    f'AND "open access"[Filter]'
)


with Entrez.esearch(
    db="pmc",
    term=search_query,
    retmax=max_papers,
    sort="relevance",
) as handle:

    result = Entrez.read(handle)


pmc_ids = result["IdList"]
print(f"Total search results: {result['Count']}")




for pmc_id in pmc_ids:

    pmcid = f"PMC{pmc_id}"
    output_file = output_dir / f"{pmcid}.json"

    if output_file.exists():
        continue

    response = requests.get(
        f"https://www.ncbi.nlm.nih.gov/research/bionlp/RESTful/pmcoa.cgi/BioC_json/{pmcid}/unicode"
    )

    output_file.write_text(
        response.text,
        encoding="utf-8",
    )

    print(f"Downloaded: {output_file.name}")

    sleep(0.4)

