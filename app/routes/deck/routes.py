from flask import Blueprint, render_template, request

from app.services.deck import create_deck, delete_all_decks, get_decks, delete_all_decks

deck_bp = Blueprint("deck_bp", __name__, url_prefix="/deck")

@deck_bp.route("/", methods=["GET"])
def index_route():
    decks = get_decks()
    return render_template("deck.html", decks=decks)

@deck_bp.route("/", methods=["POST"])
def create_deck_route():
    deck_name = request.form.get("name", "").strip()
    message = create_deck(deck_name)
    return message

@deck_bp.route("/", methods=["DELETE"])
def delete_all_decks_route():
    delete_all_decks()
    return ""
