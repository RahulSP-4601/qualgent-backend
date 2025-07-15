# QualGent Backend Coding Challenge – `qgjob` System

This repository contains a CLI tool (`qgjob`) and a backend orchestrator built in Python (FastAPI) to submit, queue, and monitor AppWright test jobs across different target environments.

---

## 🔧 Tech Stack

- **Backend**: Python + FastAPI
- **CLI**: Python + Typer
- **Queueing**: In-memory with `asyncio.Queue`, grouped by `app_version_id`
- **Job State Tracking**: In-memory dict (`jobs`)
- **CI Integration**: GitHub Actions (`test.yml`)
- **Storage**: In-memory (stateless, reset on restart)

---

## 📁 Project Structure

```
.
├── backend/
│   ├── main.py               # FastAPI server
│   ├── job_runner.py         # Job processing logic (async)
│   ├── job_queue.py          # In-memory queue structure
│   ├── state.py              # Shared in-memory job store
│   └── models.py             # Pydantic schema for job request
├── cli/
│   └── qgjob.py              # CLI Tool using Typer
├── tests/
│   └── onboarding.spec.js    # Dummy test file
├── .github/workflows/
│   └── test.yml              # GitHub Actions Workflow
├── requirements.txt
└── README.md
```

---

## 🚀 How to Run Locally

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Start the FastAPI backend

```bash
uvicorn backend.main:app --reload
```

### 3. Submit a job using the CLI

```bash
python cli/qgjob.py submit \
  --org-id=qualgent \
  --app-version-id=xyz123 \
  --test=tests/onboarding.spec.js
```

### 4. Watch job status

```bash
python cli/qgjob.py status \
  --job-id=<job_id_from_submission> \
  --watch
```

---

## 📦 Example Output

```bash
$ python cli/qgjob.py submit --org-id=qualgent --app-version-id=xyz123 --test=tests/onboarding.spec.js
{'job_id': '1234abcd...', 'status': 'queued'}

$ python cli/qgjob.py status --job-id 1234abcd... --watch
✅ running updated version...
1234abcd... → queued
1234abcd... → running
1234abcd... → completed
```

---

## 🧠 How Grouping & Scheduling Works

- Jobs are grouped by `app_version_id` and placed into separate `asyncio.Queue`s.
- A background runner continuously dequeues jobs by group.
- Only one device (simulated agent) runs jobs per group, minimizing app reinstall overhead.
- Job status transitions:
  - `queued` → held in queue
  - `running` → simulated 2-second delay
  - `completed` → job marked done

---

## ✅ GitHub Actions Integration

The project includes a GitHub Actions workflow that:

- Installs dependencies
- Runs the CLI to submit a test job
- Can be extended to poll job status and fail if needed

```yaml
name: AppWright Test
on: [push]

jobs:
  run-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: 3.10
      - run: |
          pip install -r requirements.txt
          python cli/qgjob.py submit --org-id=qualgent --app-version-id=xyz123 --test=tests/onboarding.spec.js
```

---

## 🔚 Notes

- The system is stateless — jobs are reset on restart.
- To keep things fast and simple for the challenge, no DB or persistent storage is used.
- `--watch` flag in the CLI provides real-time job tracking.
