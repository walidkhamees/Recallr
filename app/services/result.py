from datetime import datetime

from app.services.db import db
from app.services.deck import get_deck_id_from_name

def get_all_quiz_results(deck):
    deck_id, message = get_deck_id_from_name(deck)
    if message != "":
        return {}, "Error: Deck not found"

    get_all_quiz_results_stmt = """
        SELECT quiz.id, quiz.start_epoch,
        (
            select count(*) from quiz_card
            where quiz_card.quiz_id = quiz.id and quiz_card.answered = 1
        )
        as correct,
        (
            select count(*) from quiz_card
            where quiz_card.quiz_id = quiz.id and quiz_card.answered != 1
        ) as wrong
        FROM quiz
        WHERE quiz.deck_id = ? and ( quiz.status = 1 or quiz.end_epoch < ? )
        ORDER BY quiz.start_epoch DESC;
    """
    now = int(datetime.now().timestamp())
    try:
        rows = db.fetch_all(get_all_quiz_results_stmt, (deck_id, now))
    except:
        return {}, "Error: Could not get quiz results"

    results = {}
    for row in rows:
        results[row[0]] = {
            "time": datetime.fromtimestamp(row[1]).strftime("%B %d, %Y"),
            "correct": row[2],
            "wrong": row[3],
        }

    return results, ""

def get_quiz_result(quiz_id):
    """
        gets the result of a quiz
        args:
            quiz_id: the id of the quiz
        returns:
            quiz_result(dict):
            {
                "correct": number of correct answers,
                "wrong": number of wrong answers,
                "unanswered": number of unanswered cards,
                "quiz_id": id of the quiz,
                "cards": {
                    "card_id": {
                        "question": question of the card,
                        "answer": answer of the card,
                        "correct": whether the card was answered correctly or not,
                        "user_answer": answer given by the user
                    }
                    ...
                }
            }
            message: error message if there was an error
    """

    result_stmt = """
        SELECT card.id, quiz_card.answered, quiz_card.answer, card.question, card.answer as user_answer
        FROM quiz_card
        INNER JOIN card ON quiz_card.card_id = card.id
        WHERE quiz_card.quiz_id = ?
    """
    all_questions_stmt = """
        SELECT COUNT(*) FROM quiz_card
        WHERE quiz_card.quiz_id = ?;
    """

    try:
        quiz_cards = db.fetch_all(result_stmt, (quiz_id,))
        all_questions = db.fetch_one(all_questions_stmt, (quiz_id,))
    except:
        return {}, "Error: Could not get quiz result"


    correct = 0
    wrong = 0
    for card in quiz_cards:
        if card[1] == 1:
            correct += 1
        elif card[1] == -1:
            wrong += 1

    quiz_result = {
        "correct": correct,
        "wrong": wrong,
        "unanswered": all_questions[0] - correct - wrong,
        "quiz_id": quiz_id,

        "cards": {}
    }

    for card in quiz_cards:
        quiz_result["cards"][card[0]] = {
            "question": card[3],
            "answer": card[4],
            "correct": card[1] == 1,
            "user_answer": card[2],
        }

    return quiz_result, ""
