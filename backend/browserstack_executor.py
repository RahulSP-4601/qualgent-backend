import os
import requests
import subprocess
import re
from dotenv import load_dotenv

load_dotenv()

USERNAME = os.getenv("BROWSERSTACK_USERNAME")
ACCESS_KEY = os.getenv("BROWSERSTACK_ACCESS_KEY")

def run_browserstack_test(org_id, app_version_id, test_path, platform, app_id):
    try:
        print("📦 Running BrowserStack WebDriverIO test...")
        result = subprocess.run(
            ["npx", "wdio", "wdio.browserstack.conf.js"],
            check=True,
            capture_output=True,
            text=True,
            timeout=90
        )

        output = result.stdout
        print("✅ Test Output:\n", output)

        # Extract the real session ID from WebDriverIO output
        match = re.search(r"Session ID:\s+([a-z0-9]+)", output)
        if match:
            session_id = match.group(1)
            print(f"✅ Extracted session_id: {session_id}")
            return session_id
        else:
            print("⚠️ Could not extract session ID from test output.")
            return None

    except subprocess.CalledProcessError as e:
        print("❌ Test execution failed:\n", e.stderr)
        return None
    except subprocess.TimeoutExpired:
        print("⏱️ Test timed out.")
        return None

def get_browserstack_video_url(session_id):
    url = f"https://api.browserstack.com/automate/sessions/{session_id}.json"  # ✅ CORRECT ENDPOINT

    response = requests.get(url, auth=(USERNAME, ACCESS_KEY))
    if response.status_code == 200:
        data = response.json()
        video_url = data["automation_session"]["video_url"]
        print("🎥 Video URL:", video_url)
        return video_url
    else:
        print("❌ Failed to fetch video from BrowserStack:", response.text)
        return None
