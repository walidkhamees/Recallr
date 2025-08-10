from flask import Blueprint, render_template, request

# from app.services.card import answer_card
from app.services.quiz import answer_card_in_quiz, create_quiz, get_quiz_score

quiz_bp = Blueprint("quiz_bp", __name__, url_prefix="/deck/<deck>/quiz")

@quiz_bp.route("/", methods=["GET"])
def index(deck):
    quiz, message = create_quiz(deck)
    if message != "":
        return message

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

@quiz_bp.route("/<int:quiz_id>/", methods=["GET"])
def quiz_status_route(deck, quiz_id):
    status, message = get_quiz_score(quiz_id)
    if message != "":
        return message

    return render_template("quiz_status.html", deck=deck, quiz_id=quiz_id, status=status)