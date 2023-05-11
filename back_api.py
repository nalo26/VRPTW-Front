from flask import Blueprint, request
from flask_caching import Cache

bp = Blueprint("back", __name__, url_prefix="/back")
cache = None


def init(_cache: Cache):
    global cache
    cache = _cache


@bp.route("/update_graph", methods=["POST"])
def update_graph():
    data = request.get_json()
    remote_graphs = cache.get("remote_graphs")
    remote_graphs.append(data)
    cache.set("remote_graphs", remote_graphs)
    return "OK", 200
