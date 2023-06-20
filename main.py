from flask import Flask, render_template
from flask_caching import Cache
import logging

import front_api
import back_api

log = logging.getLogger("werkzeug")
log.setLevel(logging.ERROR)

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

front_api.init(cache, log)
back_api.init(cache, log)


@app.route("/")
def index():
    cache.set("remote_graphs", [])
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8090, debug=True)
