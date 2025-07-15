import typer
import requests
import time

app = typer.Typer()
API_URL = "http://localhost:8000"

@app.command()
def submit(
    org_id: str = typer.Option(..., "--org-id", "-o"),
    app_version_id: str = typer.Option(..., "--app-version-id", "-a"),
    test: str = typer.Option(..., "--test", "-t"),
    priority: int = typer.Option(1, "--priority", "-p"),
    target: str = typer.Option("emulator", "--target")
):
    payload = {
        "org_id": org_id,
        "app_version_id": app_version_id,
        "test_path": test,
        "priority": priority,
        "target": target
    }
    res = requests.post(f"{API_URL}/submit", json=payload)
    typer.echo(res.json())

@app.command()
def status(
    job_id: str = typer.Option(..., "--job-id"),
    watch: bool = typer.Option(False, "--watch", "-w")
):
    print("✅ running updated version...")

    last_status = None
    while True:
        res = requests.get(f"{API_URL}/status/{job_id}")
        if res.status_code != 200:
            typer.echo(f"❌ Failed to fetch status: {res.status_code}")
            break

        data = res.json()
        if "error" in data:
            typer.echo(f"❌ {data['error']}")
            break

        current_status = data.get("status")
        if current_status != last_status:
            typer.echo(f"{job_id} → {current_status}")
            last_status = current_status

        if not watch or current_status == "completed":
            break

        time.sleep(1)



if __name__ == "__main__":
    app()
