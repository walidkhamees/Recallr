import time
from app.utils import constants

def _get_cards_as_dict(cards):
    cards_dict = {}

    for card in cards:
        card_splited = card.split(constants.CARD_SEPRATOR)

        if len(card_splited) < 5:
            continue

        card_id = card_splited[0]
        cards_dict[card_id] = {}
        cards_dict[card_id]["question"] = card_splited[1]
        cards_dict[card_id]["answer"] = card_splited[2]
        cards_dict[card_id]["last_answered"] = card_splited[3]
        cards_dict[card_id]["correct"] = card_splited[4]

    return cards_dict


def _create_line_from_card_dict(card_id, card_dict):
    line = f"{card_id}{constants.CARD_SEPRATOR}"
    line += f"{constants.CARD_SEPRATOR}".join([
        card_dict["question"],
        card_dict["answer"],
        str(card_dict["last_answered"]),
        str(card_dict["correct"]),
    ])
    return line


def _write_all_cards(deck, cards_dict):
    deck_file = open(f"{constants.DECK_PATH}/{deck}.txt", "w")
    for card_id, card_dict in cards_dict.items():
        line = _create_line_from_card_dict(card_id, card_dict)
        deck_file.write(line + "\n")
    deck_file.close()

    return ""

def delete_card(deck, card_id):
    cards, message = get_all_cards(deck)

    if message != "":
        return message

    cards_dict = _get_cards_as_dict(cards)

    if card_id not in cards_dict:
        return "Error: Card not found"

    cards_dict.pop(card_id)
    _write_all_cards(deck, cards_dict)

    return ""






def get_all_cards(deck):
    cards = []
    try:
        deck_file = open(f"{constants.DECK_PATH}/{deck}.txt", "r")
        cards = deck_file.read().strip()
        deck_file.close()
    except FileNotFoundError:
        return cards, "Error: Deck not found"

    if cards == "":
        return cards, ""

    cards = cards.split("\n")
    return cards, ""


def create_card(deck, question, answer):
    cards, message = get_all_cards(deck)

    if message != "":
        return message

    cards_dict = _get_cards_as_dict(cards)

    card_id = str(len(cards_dict) + 1)

    while card_id in cards_dict:
        card_id = str(int(card_id) + 1)


    cards_dict[card_id] = {
        "question": question,
        "answer": answer,
        "last_answered": int(time.time()), # Gets the current epoch time
        "correct": False,
    }

    _write_all_cards(deck, cards_dict)
    return ""

def update_card(deck, card_id, new_question, new_answer):
    cards, message = get_all_cards(deck)
    cards_dict = _get_cards_as_dict(cards)

    if not card_id in cards_dict:
        return "This card doesn't exist"

    if new_question == "":
        return "Question cannot be empty"

    if new_answer == "":
        return "Answer cannot be empty"

    cards_dict[card_id]["question"] = new_question
    cards_dict[card_id]["answer"] = new_answer

    _write_all_cards(deck, cards_dict)

    return message
