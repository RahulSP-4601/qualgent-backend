from pydantic import BaseModel

class JobRequest(BaseModel):
    org_id: str
    app_version_id: str
    test_path: str
    priority: int = 1
    target: str  # emulator, device, browserstack
