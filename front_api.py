import json
from flask import Blueprint, request
from flask_caching import Cache

from file_parser import parse
from utils import send_json

bp = Blueprint("front", __name__, url_prefix="/front")
cache = None
log = None


def init(_cache: Cache, log_):
    global cache, log
    cache = _cache
    log = log_


@bp.route("/create_graph", methods=["POST"])
def update_output():
    if request.files is None:
        return "No file uploaded", 400

    upload_file = request.files["file"]
    if upload_file.filename.rsplit(".", 1)[1].lower() != "vrp":
        return "Wrong file format", 400

    data = parse(upload_file.read().decode("utf-8"))
    if "methods" in request.form:
        data["methods"] = json.loads(request.form["methods"])
    algorithm = request.form["algo"]
    params = dict(
        ((k, int(v)) for k, v in request.form.items() if not k in ("methods", "algo"))
    )
    cache.set("graph_base", data)
    send_json(data, algorithm, params)
    # log.error("------------------------------------------")
    return data, 200


@bp.route("/get_graph", methods=["GET"])
def get_graph():
    remote_graphs: list = cache.get("remote_graphs") or []
    if len(remote_graphs) == 0:
        return "No graph", 400
    graph = remote_graphs.pop(0)
    cache.set("remote_graphs", remote_graphs)
    return graph, 200
