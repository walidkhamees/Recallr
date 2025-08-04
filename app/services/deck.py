import os
import re

def get_decks():
    decks = []
    for file in os.listdir("app/decks"):
        decks.append(file.replace(".txt", ""))
    return decks

def create_deck(deck_name):
    cleaned_deck_name = re.sub(r"[[<>/?\\,:*| ]", "", deck_name)

    if cleaned_deck_name != deck_name:
        return "Deck name cannot contain special characters"

    if deck_name == "":
        return "Deck name cannot be empty"

    deck_file = open(f"app/decks/{deck_name}.txt", "w")
    deck_file.close()
    return f"Deck {deck_name} created successfully"

def get_deck(deck_name):
    deck = {
        "name": deck_name,
        "cards": {

        }
    }
    deck_file = open(f"app/decks/{deck_name}.txt", "r")
    cards = deck_file.read().split("\n")
    deck_file.close()
    for card in cards:
        card_splited = card.split("`")

        card_id = card_splited[0]
        card = {
            "question": card_splited[1],
            "answer": card_splited[2],
            "last_answered": card_splited[3],
            "correct": card_splited[4],
        }
        deck["cards"][card_id] = card

    return deck

def delete_all_decks():
    for file in os.listdir("app/decks"):
        os.remove(f"app/decks/{file}")
