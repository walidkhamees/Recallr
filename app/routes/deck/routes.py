from flask import Blueprint, render_template, request, redirect, jsonify

from app.services.deck import create_deck, delete_all_decks, get_deck, get_decks, update_deck, delete_deck
import app.utils.http_codes as HTTP_CODES


deck_bp = Blueprint("deck_bp", __name__, url_prefix="/deck")

@deck_bp.route("/", methods=["GET"])
def index_route():
    decks, message = get_decks()
    if message != "":
        return message

    print(decks)
    return render_template("decks.html", decks=decks)

@deck_bp.route("/", methods=["POST"])
def create_deck_route():
    deck_name = request.form.get("name", "").strip()
    message = create_deck(deck_name)

    if message != "":
        return message

    return redirect(f"/deck")

@deck_bp.route("/", methods=["PUT"])
def update_deck_route():
    deck_update_request = request.get_json()
    deck_name = deck_update_request["deck_name"]
    deck_id = deck_update_request["deck_id"]

    message = update_deck(deck_id, deck_name)
    if message != "":
        return jsonify({"message": message}), HTTP_CODES.BAD_REQUEST

    return jsonify({"message": "Deck updated"}), HTTP_CODES.OK


@deck_bp.route("/<int:deck_id>", methods=["DELETE"])
def delete_deck_route(deck_id):
    message = delete_deck(deck_id)
    if message != "":
        return jsonify({"message": message}), HTTP_CODES.BAD_REQUEST

    return jsonify({"message": "Deck deleted"}), HTTP_CODES.OK

@deck_bp.route("/", methods=["DELETE"])
def delete_all_decks_route():
    message = delete_all_decks()
    if message != "":
        return redirect(f"/deck", code=HTTP_CODES.SERVER_ERROR)
    return ""

@deck_bp.route("/<deck_name>", methods=["GET"])
def get_deck_route(deck_name):
    # Handle the case where the deck doesn't exist
    deck, message = get_deck(deck_name)

    if message == "":
        return render_template("deck.html", deck=deck)

    return message
