from fastapi import FastAPI
import uuid
import asyncio

from backend.models import JobRequest
from backend.job_runner import start_runner
from backend.state import queues, jobs, video_results

app = FastAPI()

@app.on_event("startup")
def on_startup():
    print("✅ FastAPI startup hook triggered.")
    asyncio.create_task(start_runner())

@app.post("/submit")
async def submit_job(job: JobRequest):
    job_id = str(uuid.uuid4())
    job_data = job.dict()
    job_data["id"] = job_id
    job_data["status"] = "queued"
    jobs[job_id] = job_data

    print(f"✅ Job {job_id} enqueued to queue {job.app_version_id}")
    await queues[job.app_version_id].put(job_id)
    return {"job_id": job_id, "status": "queued"}

@app.get("/status/{job_id}")
def check_status(job_id: str):
    job = jobs.get(job_id)
    if not job:
        return {"error": "Job not found"}
    return {"job_id": job_id, "status": job["status"]}

@app.get("/result/{job_id}")
def get_result(job_id: str):
    result = video_results.get(job_id)
    if not result:
        return {"error": "No result found for this job"}
    return result

@app.get("/debug/queues")
def debug_queues():
    return {k: q.qsize() for k, q in queues.items()}
