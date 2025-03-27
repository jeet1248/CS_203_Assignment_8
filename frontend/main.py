from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
import requests

app = FastAPI()

BACKEND_URL = "http://10.162.0.5:9567"
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/insert/{text}")
async def insert_document(text):
    response = requests.get(f"{BACKEND_URL}/insert/{text}")
    print(text)
    if response.status_code == 200:
        return response.json()
    return JSONResponse(status_code=response.status_code, content=response.json())


@app.get("/get/{query}")
async def get_best_document(query: str):
    response = requests.get(f"{BACKEND_URL}/get/{query}")
    print(query)
    if response.status_code == 200:
        return response.json()
    return JSONResponse(status_code=response.status_code, content=response.json())