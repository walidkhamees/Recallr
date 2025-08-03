import flask
import os
from flask import render_template

app = flask.Flask(
    "Flash cards Application for hobbyists",
    static_folder="static",
    template_folder="static/html"
)




@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")



if __name__ == "__main__":
    if not os.path.isdir("data"):
        os.mkdir("data")
    app.run(debug=True)
