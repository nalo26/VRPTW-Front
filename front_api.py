from flask import Blueprint, request, g

from file_parser import parse
from utils import send_json

bp = Blueprint("front", __name__, url_prefix="/front")


@bp.route("/create_graph", methods=["POST"])
def update_output():
    if request.files is None:
        return "No file uploaded", 400

    upload_file = request.files["file"]
    if upload_file.filename.rsplit(".", 1)[1].lower() != "vrp":
        return "Wrong file format", 400

    data = parse(upload_file.read().decode("utf-8"))
    g.local_graph_data = data
    send_json(data)
    return "OK", 200
