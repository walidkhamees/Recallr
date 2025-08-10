import time
from app.services.deck import get_deck_id_from_name
from app.services.card import get_card
from app.services.db import db
from app.utils import constants

def get_cards_on_answer(quiz_id, answer):
    get_cards_stmt = """
    SELECT card.id, card.question, card.answer, card.last_time_answered_epoch, card.correct
    FROM card
    INNER JOIN deck ON card.deck_id = deck.id
    WHERE deck.name = ? AND card.correct = ?
    ORDER by card.last_time_answered_epoch desc
    LIMIT ?
"""
    try:
        rows = db.fetch_all(get_cards_stmt, (quiz_id, answer, constants.CARDS_PER_QUIZ))

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

def get_last_quiz(deck):
    """
    Get the last quiz for a deck
    args:
        deck: name of the deck
    returns:
        quiz: the last quiz for the deck
        {
            "quiz_id": id of the quiz,
            "quiz_start_epoch": epoch of the start of the quiz,
            "quiz_end_epoch": epoch of the end of the quiz,
            "cards": {
                "card_id": {
                    "question": question of the card,
                    "answer": answer of the card,
                    "last_time_answered_epoch": epoch of the last time the card was answered,
                    "correct": whether the card was answered correctly or not
                }
            }
        }
        message: error message if there was an error
    """

    get_quiz_stmt = """
SELECT quiz.id, quiz.quiz_start_epoch, quiz.quiz_end_epoch
FROM quiz
INNER JOIN deck ON quiz.deck_id = deck.id
WHERE deck.name = ?
ORDER BY quiz.id DESC
LIMIT 1
"""

    get_cards_stmt = """
SELECT card.id, card.question, card.answer, card.last_time_answered_epoch, card.correct, quiz_card.answered
FROM card
INNER JOIN deck ON card.deck_id = deck.id
INNER JOIN quiz_card ON quiz_card.card_id = card.id
WHERE quiz_card.quiz_id = ?
"""

    quiz = {}
    try:
        row = db.fetch_one(get_quiz_stmt, (deck,))

        if not row:
            return {}, ""

        quiz["quiz_id"] = row[0]
        quiz["quiz_start_epoch"] = row[1]
        quiz["quiz_end_epoch"] = row[2]

        cards = {}

        rows = db.fetch_all(get_cards_stmt, (quiz["quiz_id"],))
        for row in rows:
            card_id = row[0]
            question = row[1]
            answer = row[2]
            last_answered_epoch = row[3]
            correct = row[4]
            answered = row[5]

            if answered:
                continue

            cards[card_id] = {
                "question": question,
                "answer": answer,
                "last_time_answered_epoch": last_answered_epoch,
                "correct": correct
            }

        quiz["cards"] = cards

        return quiz, ""

    except:
        return {}, "Error: Could not get last quiz"

def create_quiz(deck):
    now = int(time.time())
    after = now + constants.QUIZ_TIME

    last_quiz, message = get_last_quiz(deck)

    if message != "":
        return {}, message

    if len(last_quiz) > 0 and (now < last_quiz["quiz_end_epoch"]):
        return last_quiz, ""

    new_cards, message = get_cards_on_answer(deck, 0) 
    if message != "":
        return {}, message

    wrongly_answered_cards, message = get_cards_on_answer(deck, -1) # wrongly answered cards
    if message != "":
        return {}, message

    rightly_answered_cards, message = get_cards_on_answer(deck, 1) # rightly answered cards
    if message != "":
        return {}, message

    create_quiz_stmt = """
        INSERT INTO quiz (deck_id, quiz_start_epoch, quiz_end_epoch)
        VALUES (?, ?, ?)
    """

    quiz_id = 0

    deck_id, message = get_deck_id_from_name(deck)
    if message != "":
        return {}, message

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
    quiz["quiz_start_epoch"] = now
    quiz["quiz_end_epoch"] = after

    if len(new_cards) == 0 and len(wrongly_answered_cards) == 0 and len(rightly_answered_cards) == 0:
        db.rollback()
        return {}, "Error: No cards available for quiz"

    if len(new_cards) == constants.CARDS_PER_QUIZ:
        quiz["cards"] = new_cards
    else:
        needed_cards = constants.CARDS_PER_QUIZ - len(new_cards)
        wrongly_answered_cards = dict(list(wrongly_answered_cards.items())[:needed_cards])
        quiz["cards"] = new_cards | wrongly_answered_cards
    
    if len(quiz["cards"]) < constants.CARDS_PER_QUIZ:
        needed_cards = constants.CARDS_PER_QUIZ - len(quiz["cards"])
        rightly_answered_cards = dict(list(rightly_answered_cards.items())[:needed_cards])
        quiz["cards"] = quiz["cards"] | rightly_answered_cards

    # Reverse the order of cards to start with the most recent ones
    # quiz["cards"] = dict(list(quiz["cards"]).reverse())  


    for card_id in quiz["cards"]:
        try:
            db.execute_without_commit("INSERT INTO quiz_card (quiz_id, card_id, answered) VALUES (?, ?, ?)", (quiz_id, card_id, False))
        except:
            db.rollback()
            return {}, "Error: Could not insert cards into quiz"

    db.commit()
    return quiz, ""

def answer_card_in_quiz(quiz_id, deck, card_id, answer):
    last_quiz, message = get_last_quiz(deck)
    if message != "":
        return message

    now = int(time.time())
    answer = answer.strip().lower()

    # Check if the quiz is valid and not expired
    if len(last_quiz) == 0:
        return "Error: No quiz found"
    if last_quiz["quiz_end_epoch"] < now:
        return "Error: Quiz has ended"


    answer_card_stmt = """
        UPDATE card
        SET last_time_answered_epoch = ?, correct = ?
        WHERE id = ?
    """

    card, message = get_card(deck, card_id)
    if message != "":
        return message
    
    card["answer"] = card["answer"].strip().lower()

    correct = 1 if answer == card["answer"] else -1

    try:
        db.execute_without_commit(answer_card_stmt, (now, correct, card_id))
    except:
        db.rollback()
        return "Error: Could not answer card"

    answer_card_in_quiz_stmt = """
        UPDATE quiz_card
        SET answered = ?
        WHERE quiz_id = ? AND card_id = ?
    """

    try:
        db.execute_without_commit(answer_card_in_quiz_stmt, (correct, quiz_id, card_id))
    except:
        db.rollback()
        return "Error: Could not answer card in quiz"

    db.commit()
    return ""

def get_quiz_score(quiz_id): 
    check_is_finished_stmt = """
    SELECT COUNT(*) FROM quiz_card
    WHERE quiz_id = ? AND answered = 0
    """
    

    try:
        row = db.fetch_one(check_is_finished_stmt, (quiz_id,))
        unanswered = row[0]
        if unanswered > 0: 
            return (), "You still haven't finished the quiz"
        
    except:
        return (), "Error: Could not check quiz status"

    right_answers_stmt = """
    SELECT COUNT(*) FROM quiz_card
    WHERE quiz_id = ? AND answered = 1
    """
    wrong_answers_stmt = """
    SELECT COUNT(*) FROM quiz_card
    WHERE quiz_id = ? AND answered = -1
    """

    try:
        right_row = db.fetch_one(right_answers_stmt, (quiz_id,))
        wrong_row = db.fetch_one(wrong_answers_stmt, (quiz_id,))
        
        right_answers = right_row[0]
        wrong_answers = wrong_row[0]

        return (right_answers, wrong_answers), ""
    except:
        return (), "Error: Could not check quiz score"
