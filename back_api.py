from flask import Blueprint, request
from flask_caching import Cache

bp = Blueprint("back", __name__, url_prefix="/back")
cache = None
log = None


def init(_cache: Cache, log_):
    global cache, log
    cache = _cache
    log = log_


@bp.route("/update_graph", methods=["POST"])
def update_graph():
    data = request.get_json()
    remote_graphs = cache.get("remote_graphs")
    remote_graphs.append(data)
    log.error(
        "fitness: "
        + str(data.get("fitness"))
        + " / trucks: "
        + str(len(data.get("routes")))
    )

    cache.set("remote_graphs", remote_graphs)
    return "OK", 200
