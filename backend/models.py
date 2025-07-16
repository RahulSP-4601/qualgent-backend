from pydantic import BaseModel
from datetime import datetime

class JobRequest(BaseModel):
    org_id: str
    app_version_id: str
    test_path: str
    priority: int = 1
    target: str  # emulator, device, browserstack

class VideoResult(BaseModel):
    job_id: str
    video_url: str
    platform: str  # android, ios, etc.
    timestamp: datetime
