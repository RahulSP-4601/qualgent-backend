from pydantic import BaseModel
from datetime import datetime

class JobRequest(BaseModel):
    org_id: str
    app_version_id: str
    test_path: str
    priority: int
    target: str

class VideoResult(BaseModel):
    job_id: str
    platform: str
    video_url: str
    timestamp: datetime
