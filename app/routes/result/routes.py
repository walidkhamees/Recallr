from flask import Blueprint, render_template

from app.services.result import get_all_quiz_results, get_quiz_result
from app.utils import constants

result_bp = Blueprint("result", __name__, url_prefix="/deck/<deck>/result")

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

# route that returns quiz results as a text file
@result_bp.route("/text", methods=["GET"])
def quiz_text_results_route(deck):
    results, message = get_all_quiz_results(deck)
    if message != "":
        return message

    with open(f"{constants.RESULTS_PATH}/quiz_results.txt", "w") as f:
        f.write("Quiz ID - Time - Correct - Wrong\n")
        for quiz_id, result in results.items():
            f.write(f"{quiz_id} - {result["time"]} - {result["correct"]} - {result["wrong"]}\n")

    with open(f"{constants.RESULTS_PATH}/quiz_results.txt", "r") as f:
        return render_template("result_text.html", text=f.read())

