import time
import uuid
import asyncio
import heapq
from models import Ingestion, Batch, BatchStatus, Priority
from storage import ingestions, processing_queue

PRIORITY_MAP = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}

async def enqueue_request(ids, priority):
    ingestion_id = str(uuid.uuid4())
    created_time = time.time()
    batches = [
        Batch(batch_id=str(uuid.uuid4()), ids=ids[i:i+3], status=BatchStatus.YET_TO_START)
        for i in range(0, len(ids), 3)
    ]
    ingestion = Ingestion(
        ingestion_id=ingestion_id,
        priority=priority,
        created_time=created_time,
        batches=batches,
    )
    ingestions[ingestion_id] = ingestion
    heapq.heappush(processing_queue, (PRIORITY_MAP[priority], created_time, ingestion_id))
    return ingestion_id

async def process_loop():
    while True:
        if processing_queue:
            _, _, ingestion_id = heapq.heappop(processing_queue)
            ingestion = ingestions[ingestion_id]
            for batch in ingestion.batches:
                if batch.status == BatchStatus.YET_TO_START:
                    batch.status = BatchStatus.TRIGGERED
                    await asyncio.sleep(5)
                    for _id in batch.ids:
                        await asyncio.sleep(1)  # simulate API delay
                    batch.status = BatchStatus.COMPLETED
        await asyncio.sleep(1)

def get_ingestion_status(ingestion_id):
    ingestion = ingestions.get(ingestion_id)
    if ingestion:
        all_statuses = [b.status for b in ingestion.batches]
        if all(s == BatchStatus.YET_TO_START for s in all_statuses):
            outer_status = "yet_to_start"
        elif all(s == BatchStatus.COMPLETED for s in all_statuses):
            outer_status = "completed"
        else:
            outer_status = "triggered"
        return {
            "ingestion_id": ingestion_id,
            "status": outer_status,
            "batches": [b.dict() for b in ingestion.batches]
        }
    return None
