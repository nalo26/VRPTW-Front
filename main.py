import time
import threading

from flask import Flask, render_template
from flask_caching import Cache

import front_api
import back_api


app = Flask(__name__)
app.register_blueprint(front_api.bp)
app.register_blueprint(back_api.bp)

cache = Cache(
    app,
    config={
        "CACHE_TYPE": "SimpleCache",
        "CACHE_DEFAULT_TIMEOUT": 60 * 60,  # 1h
    },
)

front_api.init(cache)
back_api.init(cache)


@app.route("/")
def index():
    return render_template("index.html")


def background_task():
    print("Background task started")
    with app.app_context():
        while True:
            if cache.get("local_graph_data") and cache.get("remote_graph_data"):
                print("Local graph data:", cache.get("local_graph_data"))
                print("Remote graph data:", cache.get("remote_graph_data"))
            time.sleep(1)


if __name__ == "__main__":
    background = threading.Thread(target=background_task)
    background.daemon = True
    background.start()
    app.run(host="127.0.0.1", port=8050, debug=True)
