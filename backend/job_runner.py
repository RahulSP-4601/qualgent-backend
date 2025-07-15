import asyncio
from backend.job_queue import queues
from backend.state import jobs  # shared in-memory dict

async def run_jobs():
    while True:
        for app_version_id, queue in queues.items():
            if not queue.empty():
                job_id = await queue.get()

                # Simulate delay before picking up the job (keeps it in "queued")
                await asyncio.sleep(10)

                jobs[job_id]["status"] = "running"
                print(f"Job {job_id} → running")

                # Simulate execution time
                await asyncio.sleep(10)

                jobs[job_id]["status"] = "completed"
                print(f"Job {job_id} → completed")

        await asyncio.sleep(1)

def start_runner():
    loop = asyncio.get_event_loop()
    loop.create_task(run_jobs())
