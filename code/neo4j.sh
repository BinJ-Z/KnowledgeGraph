1.upload

HEAP_SIZE=2G \
"/Users/bohe/Library/Application Support/neo4j-desktop/Application/Data/dbmss/dbms-53a35dab-4054-406e-ac60-00d5b22f39c5/bin/neo4j-admin" \
database import full \
--nodes=Entity="/Users/bohe/Desktop/KnowledgeGraph/data/output_1/all_nodes.tsv" \
--relationships="/Users/bohe/Desktop/KnowledgeGraph/data/output_1/all_edges.tsv" \
--delimiter="TAB" \
--overwrite-destination=true \
knowledgegraph4

 CREATE DATABASE knowledgegraph4





2.match gut →gene→ disease

MATCH p=
(o:OrganismTaxon)
--(g:Gene)
--(d:Disease)
WHERE ALL(
    x IN nodes(p)
    WHERE single(y IN nodes(p) WHERE y = x)
)
RETURN p
LIMIT 100;

3.download



MATCH (o:OrganismTaxon)-[r1]->(g:Gene)
RETURN
    o.id AS source,
    o.name AS source_name,
    g.id AS target,
    g.name AS target_name,
    type(r1) AS interaction

UNION

MATCH (g:Gene)-[r2]->(d:Disease)
RETURN
    g.id AS source,
    g.name AS source_name,
    d.id AS target,
    d.name AS target_name,
    type(r2) AS interaction


