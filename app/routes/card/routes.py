from flask import Blueprint, request, redirect

from app.services.card import create_card

card_bp = Blueprint("card_bp", __name__, url_prefix="/deck/<deck>/card")

# @card_bp.route("/<card_id>")
# def get_card_route(card_id):
#     # TODO: implement get card route
#     return ""

@card_bp.route("/", methods=["POST"])
def create_card_route(deck):
    question = request.form.get("question", "").strip()
    answer = request.form.get("answer", "").strip()

    if question == "" or answer == "":
        return "Question and answer cannot be empty"

    message = create_card(deck, question, answer)

    if message != "":
        return message

    return redirect(f"/deck/{deck}")

