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


if __name__ == "__main__":
    cache.set("remote_graphs", [])
    app.run(host="127.0.0.1", port=8050, debug=True)
