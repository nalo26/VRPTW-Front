from flask import Blueprint, request, g

bp = Blueprint("back", __name__, url_prefix="/back")


@bp.route("/update_graph", methods=["POST"])
def update_graph():
    print("Received data")
    data = request.get_json()
    g.remote_graph_data = data
    return "OK", 200
