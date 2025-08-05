import os
import re

from app.services.card import get_all_cards
from app.utils import constants

def get_decks():
    decks = []
    for file in os.listdir(constants.DECK_PATH):
        decks.append(file.replace(".txt", ""))
    return decks

def create_deck(deck_name):
    cleaned_deck_name = re.sub(r"[[<>/?\\,:*| ]", "", deck_name)
    all_decks = get_decks()

    if cleaned_deck_name != deck_name:
        return "Deck name cannot contain special characters"

    if deck_name == "":
        return "Deck name cannot be empty"

    if deck_name in all_decks:
        return f"Deck {deck_name} already exists"

    deck_file = open(f"{constants.DECK_PATH}/{deck_name}.txt", "w")
    deck_file.close()

    return ""

def get_deck(deck_name):
    deck = {
        "name": deck_name,
        "cards": {

        }
    }
    cards, message = get_all_cards(deck_name)

    if message != "":
        return deck, message

    if len(cards) == 0:
        return deck, message

    for card in cards:
        card_splited = card.split(constants.CARD_SEPRATOR)

        if len(card_splited) < 5:
            continue

        card_id = card_splited[0]
        card = {
            "question": card_splited[1],
            "answer": card_splited[2],
            "last_answered": card_splited[3],
            "correct": card_splited[4],
        }
        deck["cards"][card_id] = card

    return deck, message

def delete_all_decks():
    for file in os.listdir(constants.DECK_PATH):
        os.remove(f"{constants.DECK_PATH}/{file}")
