import requests as rq


IP = "127.0.0.1"
PORT = 8080


def send_json(data: dict):
    print("Sending data")
    data["methods"] = ["relocate:inter", "twoOpt:intra", "exchange:inter"]
    params = {"nbIter": 500, "tabouSize": 30}
    req = rq.post(f"http://{IP}:{PORT}/tabouSearch", params=params, json=data)
    print(req.status_code)
