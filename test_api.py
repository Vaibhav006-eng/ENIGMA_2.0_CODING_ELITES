import requests
import json
import os

API_URL = "http://localhost:8001/api/upload"
filepath = "test_eeg.fif"

if not os.path.exists(filepath):
    print(f"File {filepath} not found!")
    exit(1)

print(f"Sending {filepath} to API...")
with open(filepath, "rb") as f:
    files = {"file": ("test_eeg.fif", f, "application/octet-stream")}
    try:
        response = requests.post(API_URL, files=files)
        print(f"Status Code: {response.status_code}")
        try:
            print(json.dumps(response.json(), indent=2))
        except:
            print("Response Text:", response.text)
    except Exception as e:
        print("Request failed:", e)
