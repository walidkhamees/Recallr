from flask import Blueprint, render_template, request, redirect

from app.services.quiz import answer_card_in_quiz, create_quiz

quiz_bp = Blueprint("quiz_bp", __name__, url_prefix="/deck/<deck>/quiz")

@quiz_bp.route("/", methods=["GET"])
def index(deck):
    quiz, message = create_quiz(deck)
    quiz_id = quiz["quiz_id"]

    if message != "":
        return message
    if len(quiz["cards"]) == 0:
        return redirect(f"/deck/{deck}/result/{quiz_id}")

    return render_template("quiz.html", deck=deck, quiz=quiz)

@quiz_bp.route("/", methods=["POST"])
def answer_route(deck):
    answer_request = request.get_json()

    quiz_id = answer_request["quiz_id"]
    card_id = answer_request["card_id"]
    answer = answer_request["answer"]

    message = answer_card_in_quiz(quiz_id, deck,  card_id, answer)

    if message != "":
        return message

    return ""
