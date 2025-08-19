from app.services.card import get_card
from app.services.db import db
from app.utils import constants
from app.utils.functions import get_current_epoch

def get_cards_on_answer(deck_id, answer):
    get_cards_stmt = """
        SELECT card.id, card.question, card.answer, card.last_time_answered_epoch, card.correct
        FROM card
        INNER JOIN deck ON card.deck_id = deck.id
        WHERE deck.id = ? AND card.correct = ?
        ORDER by card.last_time_answered_epoch desc
        LIMIT ?
    """
    try:
        rows = db.fetch_all(get_cards_stmt, (deck_id, answer, constants.CARDS_PER_QUIZ))

        cards = {}
        for row in rows:
            card_id = row[0]
            question = row[1]
            answer = row[2]
            last_answered_epoch = row[3]
            correct = row[4]

            cards[card_id] = {
                "question": question,
                "answer": answer,
                "last_time_answered_epoch": last_answered_epoch,
                "correct": correct
            }

        return cards, ""
    except:
        return {}, "Error: Could not get cards for quiz"

def get_last_quiz(deck_id):
    """
    Get the last quiz for a deck
    args:
        deck: name of the deck
    returns:
        quiz: the last quiz for the deck
        {
            "quiz_id": id of the quiz,
            "start_epoch": epoch of the start of the quiz,
            "end_epoch": epoch of the end of the quiz,
            "cards": {
                "card_id": {
                    "question": question of the card,
                    "answer": answer of the card,
                    "correct": correct answer of the card
                }
            }
        }
        message: error message if there was an error
    """

    get_quiz_stmt = """
        SELECT quiz.id, quiz.start_epoch, quiz.end_epoch
        FROM quiz
        INNER JOIN deck ON quiz.deck_id = deck.id
        WHERE deck.id = ?
        ORDER BY quiz.id DESC
        LIMIT 1
    """
    get_cards_stmt = """
        SELECT question, correct_answer, answer, answered, quiz_card.id
        FROM quiz_card
        WHERE quiz_card.quiz_id = ?
    """

    quiz = {}
    try:
        row = db.fetch_one(get_quiz_stmt, (deck_id,))

        if not row:
            return {}, ""

        quiz["quiz_id"] = row[0]
        quiz["start_epoch"] = row[1]
        quiz["end_epoch"] = row[2]
        cards = {}

        rows = db.fetch_all(get_cards_stmt, (quiz["quiz_id"],))
        for row in rows:
            question = row[0]
            correct = row[1]
            answer = row[2]
            answered = row[3]
            quiz_card_id = row[4]

            if answered:
                continue

            cards[quiz_card_id] = {
                "question": question,
                "answer": answer,
                "correct": correct
            }
        quiz["cards"] = cards

        return quiz, ""

    except:
        return {}, "Error: Could not get last quiz"

def create_quiz(deck_id, quiz_time):
    """
        create a new quiz or return the last quiz if it's still active
/
        args:
            deck(str): the name of the deck
        returns:
            quiz(dict):
            {
                "quiz_id": id of the quiz,
                "start_epoch": epoch of the start of the quiz,
                "end_epoch": epoch of the end of the quiz,
                "cards": {
                    "card_id": {
                        "question": question of the card,
                        "answer": answer of the card,
                        "last_time_answered_epoch": epoch of the last time the card was answered,
                        "correct": whether the card was answered correctly or not
                    }
                }
            }
            message(str): error message if there was an error
    """

    now = get_current_epoch()
    quiz_time = int(quiz_time)
    if quiz_time <= 0:
        return {}, "Error: Quiz time must be greater than 0"

    after = now + quiz_time

    last_quiz, message = get_last_quiz(deck_id)

    if message != "":
        return {}, message

    if len(last_quiz) > 0 and (now < last_quiz["end_epoch"]) and len(last_quiz["cards"]) > 0:
        return last_quiz, ""

    new_cards, message = get_cards_on_answer(deck_id, 0) # new cards
    if message != "":
        return {}, message

    wrongly_answered_cards, message = get_cards_on_answer(deck_id, -1) # wrongly answered cards
    if message != "":
        return {}, message

    rightly_answered_cards, message = get_cards_on_answer(deck_id, 1) # rightly answered cards
    if message != "":
        return {}, message

    create_quiz_stmt = """
        INSERT INTO quiz (deck_id, start_epoch, end_epoch)
        VALUES (?, ?, ?)
    """

    quiz_id = 0

    try:
        cur = db.execute_without_commit(create_quiz_stmt, (deck_id, now, after))
        quiz_id = cur.lastrowid
    except:
        db.rollback()
        return {}, "Error: Could not create quiz"

    if quiz_id == None:
        db.rollback()
        return {}, "Error: Could not create quiz"

    quiz = {}
    quiz["quiz_id"] = quiz_id
    quiz["start_epoch"] = now
    quiz["end_epoch"] = after

    if len(new_cards) == 0 and len(wrongly_answered_cards) == 0 and len(rightly_answered_cards) == 0:
        db.rollback()
        return {}, "Error: No cards available for quiz"

    quiz_cards = []
    new_cards = list(new_cards.items())
    if len(new_cards) == constants.CARDS_PER_QUIZ:
        quiz_cards = new_cards
    else:
        needed_cards = constants.CARDS_PER_QUIZ - len(new_cards)
        wrongly_answered_cards = list(wrongly_answered_cards.items())[:needed_cards]
        quiz_cards = new_cards + wrongly_answered_cards

    if len(quiz_cards) < constants.CARDS_PER_QUIZ:
        needed_cards = constants.CARDS_PER_QUIZ - len(quiz_cards)
        rightly_answered_cards = list(rightly_answered_cards.items())[:needed_cards]
        quiz_cards = quiz_cards + rightly_answered_cards


    quiz["cards"] = {}
    for card_id, card in quiz_cards:
        try:
            cur = db.execute_without_commit("INSERT INTO quiz_card (quiz_id, answered, question, correct_answer) VALUES (?, ?, ?, ?)", (quiz_id, False, card["question"], card["answer"] ))
            quiz["cards"][cur.lastrowid] = {
                "question": card["question"],
                "answer": card["answer"],
                "correct": card["correct"]
            }
        except:
            db.rollback()
            return {}, "Error: Could not insert cards into quiz"

    db.commit()
    return quiz, ""

def answer_card_in_quiz(quiz_id, quiz_card_id,  deck_id, answer):
    last_quiz, message = get_last_quiz(deck_id)
    if message != "":
        return message

    now = get_current_epoch()
    answer = answer.strip().lower()

    # Check if the quiz is valid and not expired
    if len(last_quiz) == 0:
        return "Error: No quiz found"
    if last_quiz["end_epoch"] < now:
        return "Error: Quiz has ended"

    # Check if the card is valid and not already answered
    get_quiz_card_stmt = """
      SELECT quiz_card.id, quiz_card.answered, quiz_card.question, quiz_card.correct_answer
      FROM quiz_card
      WHERE quiz_card.quiz_id = ? AND quiz_card.id = ? AND quiz_card.answered = 0
    """

    quiz_card = db.fetch_one(get_quiz_card_stmt, (quiz_id, quiz_card_id))
    if quiz_card == None:
        return "Error: Card not found"
    elif quiz_card[1] != 0:
        return "Error: Card already answered"

    question = quiz_card[2]
    correct_answer = quiz_card[3]

    answer_card_stmt = """
        UPDATE card
        SET last_time_answered_epoch = ?, correct = ?
        WHERE question = ?
    """



    correct = 1 if answer.strip().lower() == correct_answer.strip().lower() else -1

    try:
        db.execute_without_commit(answer_card_stmt, (now, correct, question))
    except:
        db.rollback()
        return "Error: Could not answer card"

    answer_card_in_quiz_stmt = """
        UPDATE quiz_card
        SET (answered, answer, correct_answer) = (?, ?, ?)
        WHERE quiz_id = ? AND id = ?
    """

    try:
        db.execute_without_commit(answer_card_in_quiz_stmt, (correct, answer, correct_answer, quiz_id, quiz_card_id))
    except:
        db.rollback()
        return "Error: Could not answer card in quiz"

    db.commit()
    return ""
