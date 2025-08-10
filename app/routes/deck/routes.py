from flask import Blueprint, render_template, request, redirect

from app.services.deck import create_deck, delete_all_decks, get_deck, get_decks

# from app.services.deck import create_deck, delete_all_decks, get_deck, get_decks, delete_all_decks

deck_bp = Blueprint("deck_bp", __name__, url_prefix="/deck")

@deck_bp.route("/", methods=["GET"])
def index_route():
    decks = get_decks()
    return render_template("decks.html", decks=decks)

@deck_bp.route("/", methods=["POST"])
def create_deck_route():
    deck_name = request.form.get("name", "").strip()
    message = create_deck(deck_name)

    if message != "":
        return message

    return redirect(f"/deck")


@deck_bp.route("/", methods=["DELETE"])
def delete_all_decks_route():
    delete_all_decks()
    return ""

@deck_bp.route("/<deck_name>", methods=["GET"])
def get_deck_route(deck_name):
    # Handle the case where the deck doesn't exist
    deck, message = get_deck(deck_name)

    if message == "":
        return render_template("deck.html", deck=deck)

    return message
