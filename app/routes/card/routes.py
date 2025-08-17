from flask import Blueprint, jsonify, redirect, request
from app.services.card import create_card, delete_all_cards, delete_card, update_card
import app.utils.http_codes as HTTP_CODES

card_bp = Blueprint("card_bp", __name__, url_prefix="/deck/<deck_id>/card")

@card_bp.route("/", methods=["POST"])
def create_card_route(deck_id):
    question = request.form.get("question", "").strip()
    answer = request.form.get("answer", "").strip()

    if question == "" or answer == "":
        return "Question and answer cannot be empty"

    message = create_card(deck_id, question, answer)
    if message != "":
        return message

    return redirect(f"/deck/{deck_id}")

@card_bp.route("/<card_id>", methods=["DELETE"])
def delete_card_route(deck_id, card_id):
    message = delete_card(deck_id, card_id)
    if message != "":
        return jsonify({"message": message}), HTTP_CODES.BAD_REQUEST

    return jsonify({"message": "Card deleted"}), HTTP_CODES.OK

@card_bp.route("/", methods=["DELETE"])
def delete_all_cards_route(deck_id):
    message = delete_all_cards(deck_id)
    if message != "":
        return jsonify({"message": message}), HTTP_CODES.BAD_REQUEST

    return jsonify({"message": "All cards deleted"}), HTTP_CODES.OK


@card_bp.route("/", methods=["PUT"])
def update_card_route(deck_id):
    data = request.get_json()

    card_id = data["card_id"]
    question = data["question"]
    answer = data["answer"]

    message = update_card(deck_id, card_id, question, answer)
    if not message == "":
        return jsonify({"message": message}), HTTP_CODES.BAD_REQUEST

    return jsonify({"message": "Card updated"}), HTTP_CODES.OK

