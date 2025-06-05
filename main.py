from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import asyncio

from processor import enqueue_request, get_ingestion_status, process_loop
from models import Priority

app = FastAPI()

class IngestionRequest(BaseModel):
    ids: List[int]
    priority: Priority

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(process_loop())

@app.get("/")
async def root():
    return {"message": "API is working"}

@app.post("/ingest")
async def ingest(data: IngestionRequest):
    try:
        ingestion_id = await enqueue_request(data.ids, data.priority)
        return {"ingestion_id": ingestion_id}
    except Exception as e:
        print(f"Error in /ingest: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/status/{ingestion_id}")
async def status(ingestion_id: str):
    result = get_ingestion_status(ingestion_id)
    if result:
        return result
    raise HTTPException(status_code=404, detail="Ingestion ID not found")
