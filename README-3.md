# 🚀 QualGent Backend Coding Challenge – `qgjob` System

This repository contains a scalable backend orchestrator and CLI tool to **submit**, **queue**, **execute**, and **monitor** AppWright test jobs on various platforms — including BrowserStack, Android, and iOS — using Python and FastAPI.

---

## ⚙️ Tech Stack

- **Backend**: FastAPI (Python)
- **CLI Tool**: Typer (Python)
- **Queueing**: In-memory `asyncio.Queue` grouped by `app_version_id`
- **Job State Tracking**: In-memory dictionary (`jobs`)
- **Video Storage**: Persisted in **MySQL**
- **CI/CD**: GitHub Actions (`test.yml`)

---

## 🗂️ Project Structure

```
.
├── backend/
│   ├── main.py                    # FastAPI entry point
│   ├── job_runner.py              # Background job runner (async)
│   ├── state.py                   # In-memory job + queue storage
│   ├── db/
│   │   ├── session.py             # SQLAlchemy DB session
│   │   └── __init__.py            # DB model registration
│   ├── models/
│   │   ├── job_model.py           # Pydantic model for job submission
│   │   └── video_result_model.py  # SQLAlchemy + Pydantic models for video result
├── cli/
│   └── qgjob.py                   # CLI using Typer
├── tests/
│   └── onboarding.spec.js         # Sample AppWright test
├── .github/workflows/
│   └── test.yml                   # GitHub Actions workflow
├── requirements.txt
└── README.md
```

---

## 🧪 How It Works

1. Jobs are submitted via a CLI or REST API.
2. Each `app_version_id` has its own async job queue.
3. A background job runner:
   - Picks up jobs.
   - Executes them via WebDriverIO on BrowserStack.
   - Retrieves the session's video URL.
   - Stores it in a **MySQL database**.

---

## 🐳 How to Run Locally

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Set environment variables in `.env`

```env
DATABASE_URL=mysql+pymysql://root:Rahul%40009@localhost/QualGent
BROWSERSTACK_USERNAME=your_username
BROWSERSTACK_ACCESS_KEY=your_access_key
BROWSERSTACK_APP_ID=bs://your_app_id
```

### 3. Start the backend server

```bash
uvicorn backend.main:app --reload
```

---

## 🧑‍💻 Submit a Job via CLI

### Submit

```bash
python cli/qgjob.py submit \
  --org-id=qualgent \
  --app-version-id=xyz123 \
  --test=tests/onboarding.spec.js \
  --target=browserstack
```

### Track Status

```bash
python cli/qgjob.py status --job-id <job_id> --watch
```

---

## ✅ Example CLI Output

```bash
$ python cli/qgjob.py submit --org-id=qualgent --app-version-id=xyz123 --test=tests/onboarding.spec.js
{'job_id': '1234abcd...', 'status': 'queued'}

$ python cli/qgjob.py status --job-id 1234abcd... --watch
👉 Processing job: 1234abcd...
✅ Job completed: https://automate.browserstack.com/sessions/abc123/video
```

---

## 🎥 Video Result Storage

After test completion, the system:

- Fetches the session video URL from BrowserStack.
- Stores it in the `video_results` table in MySQL:

```sql
CREATE TABLE video_results (
    job_id VARCHAR(255) PRIMARY KEY,
    platform VARCHAR(50),
    video_url TEXT,
    timestamp DATETIME
);
```

---

## 📦 GitHub Actions CI

Automated workflow for validating test jobs on every push:

```yaml
name: AppWright Test

on: [push]

jobs:
  run-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v4
        with:
          python-version: 3.10
      - run: |
          pip install -r requirements.txt
          python cli/qgjob.py submit \
            --org-id=qualgent \
            --app-version-id=xyz123 \
            --test=tests/onboarding.spec.js
```

---

## 🧠 Design Highlights

- **Concurrency**: Each version queue runs independently via asyncio.
- **Platform Support**: `target` supports `browserstack`, `android`, `ios`.
- **Video Fetching**: BrowserStack session videos retrieved via API.
- **Persistence**: Job metadata and video links stored in MySQL.
- **Watch Mode**: Real-time updates with `--watch` CLI flag.

---

## 📝 Final Notes

- ✅ System is now **persistent** thanks to MySQL storage.
- 🧪 Tested across **browser**, **iOS**, and **Android** targets.
- 💡 Bonus: Can be horizontally scaled using containers and deployed to cloud platforms.
