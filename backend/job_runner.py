import asyncio
from backend.job_queue import queues
from backend.state import jobs  # shared in-memory dict

async def run_jobs():
    while True:
        for app_version_id, queue in queues.items():
            if not queue.empty():
                job_id = await queue.get()

                # Optional delay to keep it in 'queued' state for a bit
                await asyncio.sleep(1)

                jobs[job_id]["status"] = "running"
                await asyncio.sleep(2)  # simulate execution
                jobs[job_id]["status"] = "completed"

        await asyncio.sleep(1)

def start_runner():
    loop = asyncio.get_event_loop()
    loop.create_task(run_jobs())
