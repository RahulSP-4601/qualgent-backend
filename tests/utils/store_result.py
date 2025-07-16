import requests

def store_result(video_url, status):
    res = requests.post("http://localhost:8000/results", json={
        "video_url": video_url,
        "status": status
    })
    print(res.json())
