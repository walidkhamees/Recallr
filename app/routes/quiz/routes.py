from flask import Blueprint, render_template

quiz_bp = Blueprint("quiz_bp", __name__, url_prefix="/deck/<deck>/quiz")

@quiz_bp.route("/")
def index():
    cards_for_quiz = get_random_cards_for_quiz()
    return render_template("quiz.html", cards_for_quiz=cards_for_quiz)
