import os



def get_decks():
    decks = []
    for file in os.listdir("app/decks"):
        decks.append(file.replace(".txt", ""))
    return decks
