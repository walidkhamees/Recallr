from flask import Blueprint, flash, redirect, render_template
from flask_login import login_required

from app.services.deck import get_deck_by_id
from app.services.result import get_all_quiz_results, get_quiz_result
from app.utils import constants

result_bp = Blueprint("result", __name__, url_prefix="/deck/<int:deck_id>/result")

@result_bp.route("/<int:quiz_id>", methods=["GET"])
@login_required
def quiz_result_route(deck_id, quiz_id):
    result, message = get_quiz_result(deck_id, quiz_id)
    if message != "":
        flash(message)
        return redirect(f"/deck/{deck_id}/result")

    deck, message = get_deck_by_id(deck_id)
    if message != "":
        flash(message)
        return redirect(f"/deck/{deck_id}/result")

    return render_template("quiz_result.html", result=result, deck=deck, deck_id=deck_id)

@result_bp.route("/", methods=["GET"])
@login_required
def quiz_results_route(deck_id):
    results, message = get_all_quiz_results(deck_id)
    if message != "":
        flash(message)
        return redirect(f"/deck/{deck_id}/result")

    deck, message = get_deck_by_id(deck_id)
    if message != "":
        flash(message)
        return redirect(f"/deck/{deck_id}/result")

    return render_template("quizzes_results.html", results=results, deck=deck, deck_id=deck_id)

# route that returns quiz results as a text file
@result_bp.route("/text", methods=["GET"])
@login_required
def quiz_text_results_route(deck_id):
    results, message = get_all_quiz_results(deck_id)
    if message != "":
        flash(message)
        return redirect(f"/deck/{deck_id}/result")

    with open(f"{constants.RESULTS_PATH}/quiz_results.txt", "w") as f:
        f.write("Quiz ID - Time - Correct - Wrong\n")
        for quiz_id, result in results.items():
            f.write(f"{quiz_id} - {result["time"]} - {result["correct"]} - {result["wrong"]}\n")

    with open(f"{constants.RESULTS_PATH}/quiz_results.txt", "r") as f:
        return render_template("result_text.html", text=f.read())
