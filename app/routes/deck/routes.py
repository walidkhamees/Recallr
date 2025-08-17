from flask import Blueprint, flash, render_template, request, redirect, jsonify
from flask_login import login_required

from app.services.deck import create_deck, delete_all_decks, get_deck, get_decks, update_deck, delete_deck
import app.utils.http_codes as HTTP_CODES


deck_bp = Blueprint("deck_bp", __name__, url_prefix="/deck")

@deck_bp.route("/", methods=["GET"])
@login_required
def index_route():
    decks, message = get_decks()
    if message != "":
        return message

    return render_template("decks.html", decks=decks)

@deck_bp.route("/", methods=["POST"])
@login_required
def create_deck_route():
    deck_name = request.form.get("name", "").strip()

    message = create_deck(deck_name)
    if message != "":
        flash(message)

    return redirect(f"/deck")

@deck_bp.route("/", methods=["PUT"])
@login_required
def update_deck_route():
    deck_update_request = request.get_json()
    deck_name = deck_update_request["deck_name"]
    deck_id = deck_update_request["deck_id"]

    message = update_deck(deck_id, deck_name)
    if message != "":
        return jsonify({"message": message}), HTTP_CODES.BAD_REQUEST

    return jsonify({"message": "Deck updated"}), HTTP_CODES.OK


@deck_bp.route("/<int:deck_id>", methods=["DELETE"])
@login_required
def delete_deck_route(deck_id):
    message = delete_deck(deck_id)
    if message != "":
        return jsonify({"message": message}), HTTP_CODES.BAD_REQUEST

    return jsonify({"message": "Deck deleted"}), HTTP_CODES.OK

@deck_bp.route("/", methods=["DELETE"])
@login_required
def delete_all_decks_route():
    message = delete_all_decks()
    if message != "":
        return jsonify({"message": message}), HTTP_CODES.BAD_REQUEST

    return jsonify({"message": "All decks deleted"}), HTTP_CODES.OK

@deck_bp.route("/<int:deck_id>", methods=["GET"])
@login_required
def get_deck_route(deck_id):
    deck, message = get_deck(deck_id)
    if message != "":
        flash(message)
        return redirect(f"/deck")

    return render_template("deck.html", deck=deck)
