from file_parser import parse
import requests as rq

IP = "localhost"
PORT = 5000


def main():
    data = parse("data/data101.vrp")
    rq.post(f"http://{IP}:{PORT}/", json=data)


if __name__ == "__main__":
    main()
