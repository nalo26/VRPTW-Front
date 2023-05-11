from flask import Flask, render_template

from front_api import bp as front_bp
from back_api import bp as back_bp


app = Flask(__name__)
app.register_blueprint(front_bp)
app.register_blueprint(back_bp)


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8050, debug=True)
