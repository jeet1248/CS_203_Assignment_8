from fastapi import FastAPI, HTTPException
from elasticsearch import Elasticsearch
from uuid import uuid4
import uvicorn
import os

app = FastAPI()

ES_HOST = os.getenv("ES_HOST", "elasticsearch")
es = Elasticsearch(ES_HOST)
INDEX_NAME = "documents"

def add_initial():
    if not es.indices.exists(index=INDEX_NAME):
        es.indices.create(index=INDEX_NAME, body={
            "mappings": {
                "properties": {
                    "id": {"type": "keyword"},
                    "text": {"type": "text"}
                }
            }
        })

add_initial()

@app.get("/get/{query}")
async def get_best_document(query: str):
    try:
        response = es.search(index=INDEX_NAME, body={
            "query": {"match": {"text": query}}
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"hits": response["hits"]["hits"]}

@app.get("/insert/{text}")
async def insert_document(text: str):
    doc_id = str(uuid4())
    doc = {"id": doc_id, "text": text}
    try:
        response = es.index(index=INDEX_NAME, id=doc_id, document=doc)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"result": response["result"], "id": doc_id}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=9567, reload=True)