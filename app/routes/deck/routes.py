from flask import Blueprint, render_template, request

deck_bp = Blueprint("deck_bp", __name__, url_prefix="/deck")

@deck_bp.route("/", methods=["GET"])
def index():
    return render_template("deck.html")


@deck_bp.route("/", methods=["POST"])
def create_deck():
    # put a confirm message here
    deck_name = request.form.get("name", "").strip()
    return deck_name
