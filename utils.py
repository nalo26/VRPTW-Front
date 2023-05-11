import requests as rq


IP = "127.0.0.1"
PORT = 8080


def send_json(data: dict):
    print("Sending data")
    req = rq.post(f"http://{IP}:{PORT}/exchange/intra", json=data)
    print(req.status_code)
