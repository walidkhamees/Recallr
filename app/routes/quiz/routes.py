from flask import Blueprint, render_template, request, redirect, flash

from app.services.deck import get_deck_by_id
from app.services.quiz import answer_card_in_quiz, create_quiz

quiz_bp = Blueprint("quiz_bp", __name__, url_prefix="/deck/<int:deck_id>/quiz")

@quiz_bp.route("/", methods=["GET"])
def index(deck_id):
    quiz_time = request.args.get("quiz_time", "30")
    if not quiz_time.isdigit():
        return "Error: Quiz time must be a number"

    try:
        quiz_time = int(quiz_time)
    except:
        return "Error: Quiz time must be a number"

    quiz, message = create_quiz(deck_id, quiz_time)
    if message != "":
        flash(message)
        return redirect(f"/deck/{deck_id}")

    quiz_id = quiz["quiz_id"]
    if len(quiz["cards"]) == 0:
        return redirect(f"/deck/{deck_id}/result/{quiz_id}")

    deck, message = get_deck_by_id(deck_id)
    if message != "":
        flash(message)
        return redirect(f"/deck/{deck_id}")

    return render_template("quiz.html", deck_id=deck_id, deck=deck, quiz=quiz)

@quiz_bp.route("/", methods=["POST"])
def answer_route(deck_id):
    answer_request = request.get_json()

    quiz_id = answer_request["quiz_id"]
    answer = answer_request["answer"]
    quiz_card_id = answer_request["quiz_card_id"]

    message = answer_card_in_quiz(quiz_id, quiz_card_id, deck_id, answer)
    if message != "":
        return message

    return ""
