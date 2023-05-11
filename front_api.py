from flask import Blueprint, request
from flask_caching import Cache

from file_parser import parse
from utils import send_json

bp = Blueprint("front", __name__, url_prefix="/front")
cache = None


def init(_cache: Cache):
    global cache
    cache = _cache


@bp.route("/create_graph", methods=["POST"])
def update_output():
    if request.files is None:
        return "No file uploaded", 400

    upload_file = request.files["file"]
    if upload_file.filename.rsplit(".", 1)[1].lower() != "vrp":
        return "Wrong file format", 400

    data = parse(upload_file.read().decode("utf-8"))
    cache.set("graph_base", data)
    send_json(data)
    return data, 200


@bp.route("/get_graph", methods=["GET"])
def get_graph():
    remote_graphs: list = cache.get("remote_graphs") or []
    if len(remote_graphs) == 0:
        return "No graph", 400
    graph = remote_graphs.pop(0)
    cache.set("remote_graphs", remote_graphs)
    return graph, 200
