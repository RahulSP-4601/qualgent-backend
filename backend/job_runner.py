import asyncio
from datetime import datetime
import os
from sqlalchemy.orm import Session
from backend.state import queues
from backend.state import jobs, video_results
from backend.db.session import SessionLocal
from backend.browserstack_executor import run_browserstack_test, get_browserstack_video_url
from backend.models.video_result_model import VideoResult, VideoResultDB

APP_ID = os.getenv("BROWSERSTACK_APP_ID")

def save_to_db(result: VideoResult):
    db: Session = SessionLocal()
    try:
        db_result = VideoResultDB(**result.dict())
        db.add(db_result)
        db.commit()
        print("🗄️ Video result saved to DB")
    except Exception as e:
        print(f"❌ DB Error: {e}")
        db.rollback()
    finally:
        db.close()

async def run_jobs():
    print("🔄 Starting job runner loop...")
    while True:
        for app_version_id, queue in queues.items():
            print(f"📥 Queue [{app_version_id}] size: {queue.qsize()}")

            if not queue.empty():
                job_id = await queue.get()
                print(f"👉 Processing job: {job_id}")
                
                try:
                    jobs[job_id]["status"] = "running"
                    print(f"🚀 Job {job_id} → running")

                    session_id = run_browserstack_test(
                        org_id=jobs[job_id]["org_id"],
                        app_version_id=jobs[job_id]["app_version_id"],
                        test_path=jobs[job_id]["test_path"],
                        platform=jobs[job_id]["target"],
                        app_id=APP_ID
                    )

                    jobs[job_id]["status"] = "completed"
                    print(f"✅ Job {job_id} → completed")

                    video_url = get_browserstack_video_url(session_id, jobs[job_id]["target"])
                    if not video_url:
                        video_url = f"https://browserstack.com/mock-video/{job_id}"

                    result_obj = VideoResult(
                        job_id=job_id,
                        video_url=video_url,
                        platform=jobs[job_id]["target"],
                        timestamp=datetime.utcnow()
                    )

                    video_results[job_id] = result_obj.dict()
                    save_to_db(result_obj)

                except Exception as e:
                    print(f"❌ Error while processing job {job_id}: {e}")
                    jobs[job_id]["status"] = "failed"

        await asyncio.sleep(1)

async def start_runner():
    await run_jobs()
