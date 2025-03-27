from elasticsearch import Elasticsearch

es = Elasticsearch([{"host": "elasticsearch", "port": 9567, "scheme": "http"}])
index_name = "documents"

if not es.indices.exists(index=index_name):
    mapping = {
        "mappings": {
            "properties": {
                "id": { "type": "keyword" },
                "text": { "type": "text" }
            }
        }
    }
    es.indices.create(index=index_name, body=mapping)
    print(f"Index '{index_name}' created.")

paragraphs = [
    "Paragraph 1: Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
    "Paragraph 2: Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
    "Paragraph 3: Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris.",
    "Paragraph 4: Duis aute irure dolor in reprehenderit in voluptate velit esse cillum."
]

for i, para in enumerate(paragraphs, start=1):
    doc = {"id": str(i), "text": para}
    res = es.index(index=index_name, id=str(i), body=doc)
    print(f"Inserted document {i}: {res}")

es.indices.refresh(index=index_name)
res = es.search(index=index_name, body={"query": {"match_all": {}}})
print("Search results:")
print(res)