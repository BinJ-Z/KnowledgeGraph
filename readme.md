


Folder 

├── code/   (RunAll.py   download_jcon.py   eight_run_all.py    neo4j.sh)
│
├── database/  
│ 
├── database_normalization/
├   ├── TAXDUMP
│   ├── HMDB
│   ├── GENE
│   ├── PROTEIN
│   └── DISEASE
│
├── data/ （source and output file）




Step：

1. Download the appendix tables of published papers (stored in data/source_3; downloaded papers are from paperinfo.xlsx).

2. Set up the object, subject, and predicate  in the xlsx file.

3. Filter papers from PubMed and download BioC format files (run download_jcon.py).

4. Perform knowledge extraction using GLiNER-RelEx (run RunAll.py).

5. Standardize the knowledge extraction data from the appendix tables and text, match it to the database, obtain IDs, and summarize to obtain the final edges file (run eight_run_all.py).

6. Import neo4j (neo4j.sh).



Requirements and Information

1.Must be an Excel file （.xlsx）format as below(lowercase is required, position are arbitrary)
subject,  object，   predicate
lactete,  diabetes,  associate

2.All .xlsx files stored in the same folder,e.g, /Users/bohe/Desktop/KnowledgeGraph/data/source_3

3.all_nodes.tsv is sourced from 5 databases(NCBI Taxonomy,NCBI GENE ,MONDO,HMDB,Uniprot protein).

4.all_edges.tsv ---Knowledge extract from a published paper, plus the conclusion section of a PubMed article.






