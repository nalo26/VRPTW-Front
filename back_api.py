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
    cache.set("remote_graph_data", data)
    return "OK", 200
