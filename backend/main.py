from fastapi import FastAPI
from pydantic import BaseModel
import uuid
import asyncio

from backend.models import JobRequest
from backend.job_runner import start_runner
from backend.state import jobs
from backend.job_queue import queues

app = FastAPI()
start_runner()  # start background job processor

@app.post("/submit")
async def submit_job(job: JobRequest):
    job_id = str(uuid.uuid4())
    job_data = job.dict()
    job_data["id"] = job_id
    job_data["status"] = "queued"
    jobs[job_id] = job_data

    await queues[job.app_version_id].put(job_id)

    return {"job_id": job_id, "status": "queued"}

@app.get("/status/{job_id}")
def check_status(job_id: str):
    job = jobs.get(job_id)
    if not job:
        return {"error": "Job not found"}
    return {"job_id": job_id, "status": job["status"]}
