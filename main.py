import base64
import requests as rq

# import pandas as pd
import plotly.graph_objects as go
from flask import Flask, request
from dash import Dash, dcc, html
from dash.dependencies import Input, Output

from file_parser import parse

IP = "127.0.0.1"
PORT = 8080

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
server = Flask(__name__)
app = Dash(
    __name__,
    server=server,
    external_stylesheets=external_stylesheets,
    update_title=None,
)

graph = None
local_graph_data = None
remote_graph_data = None

app.layout = html.Div(
    [
        html.H1("VRP"),
        dcc.Upload(
            id="input_file",
            multiple=False,
            children=html.Div(["Drag and Drop or ", html.A("Select Files")]),
        ),
        html.Div(id="hidden-output", style={"display": "none"}),
        html.Div(id="output-graph"),
        html.Div(
            [
                html.Span("Fitness: "),
                html.Span(id="output-fitness"),
            ]
        ),
        dcc.Interval(
            id="graph-update",
            interval=1000,
        ),
    ]
)


def send_json(data: dict):
    print("Sending data")
    req = rq.post(f"http://{IP}:{PORT}/random", json=data)
    print(req.status_code)


@server.route("/update_graph", methods=["POST"])
def receive_json():
    global remote_graph_data
    print("Received data")
    data = request.get_json()
    remote_graph_data = data
    return "OK", 200


@app.callback(Output("hidden-output", "children"), Input("input_file", "contents"))
def update_output(content):
    global local_graph_data
    if content is not None:
        content_type, content_string = content.split(",")
        decoded = base64.b64decode(content_string)
        data = parse(decoded.decode("utf-8"))
        local_graph_data = data
        send_json(data)
        return "Updating..."


@app.callback(
    Output("output-fitness", "children"), Input("graph-update", "n_intervals")
)
def get_fitness(n_intervals):
    if remote_graph_data is None:
        return "N/A"
    return remote_graph_data["fitness"]


@app.callback(Output("output-graph", "children"), Input("graph-update", "n_intervals"))
def get_graph(n_intervals):
    global graph
    if remote_graph_data is None:
        return graph

    traces = []

    routes = remote_graph_data["routes"]
    colors = ["red", "green", "blue", "yellow", "orange", "purple", "pink", "brown"]
    for i, route in enumerate(routes):
        x = [c.get("x") for c in route["route"]]
        y = [c.get("y") for c in route["route"]]
        traces.append(
            go.Scatter(
                x=x,
                y=y,
                mode="lines+markers",
                line=dict(width=2, color=colors[i % len(colors)]),
                name=f"Route #{i+1}",
            )
        )

    ids = [p.get("id_name") for p in local_graph_data["clients"]]
    x = [p.get("x") for p in local_graph_data["clients"]]
    y = [p.get("y") for p in local_graph_data["clients"]]
    traces.append(
        go.Scatter(
            x=x,
            y=y,
            mode="markers",
            marker=dict(color="black"),
            name="Clients",
            text=ids,
        )
    )

    graph = dcc.Graph(figure=go.Figure(data=traces))
    return graph


if __name__ == "__main__":
    app.run_server(debug=True)
