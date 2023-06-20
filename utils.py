import requests as rq


IP = "127.0.0.1"
PORT = 8091


def send_json(data: dict, algorithm: str, params: dict):
    algorithm = algorithm.replace(":", "/")
    url = f"http://{IP}:{PORT}/{algorithm}"
    print("Sending data to ", url)
    req = rq.post(url, params=params, json=data)
    print(req.status_code)
