from flask import Blueprint, render_template

main_bp = Blueprint("main_bp", __name__, url_prefix="/")

@main_bp.route("/")
def index():
    return render_template("index.html")

@main_bp.route("/help")
def help():
    return render_template("help.html")

