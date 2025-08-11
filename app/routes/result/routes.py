from flask import Blueprint, render_template

from app.services.result import get_all_quiz_results, get_quiz_result


result_bp = Blueprint('result', __name__, url_prefix='/deck/<deck>/result')

@result_bp.route("/<int:quiz_id>", methods=["GET"])
def quiz_result_route(deck, quiz_id):
    result, message = get_quiz_result(quiz_id)
    if message != "":
        return message
    return render_template("quiz_result.html", result=result, deck=deck)

@result_bp.route("/", methods=["GET"])
def quiz_results_route(deck):
    results, message = get_all_quiz_results(deck)
    if message != "":
        return message
    return render_template("quizzes_results.html", deck=deck, results=results)
