import requests
import time

url = "http://localhost:8000"

def test_priority():
    url = "http://127.0.0.1:8000"

    r1 = requests.post(f"{url}/ingest", json={"ids": [1, 2, 3, 4, 5], "priority": "MEDIUM"})
    r2 = requests.post(f"{url}/ingest", json={"ids": [6, 7, 8, 9], "priority": "HIGH"})

    print("Status 1:", r1.status_code, "Response:", r1.text)
    print("Status 2:", r2.status_code, "Response:", r2.text)


if __name__ == "__main__":
    test_priority()