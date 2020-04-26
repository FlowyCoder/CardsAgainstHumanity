import json
from os import path

def load_decks(decks, lang):
    black_cards = []
    white_cards = []

    for deck in decks:
        print("Loading File: ", path.dirname(__file__) + "/../decks/{0}/{1}.txt".format(lang, deck))
        f = open(path.dirname(__file__) + "/../decks/{0}/{1}.txt".format(lang, deck), "r", encoding="utf-8")
        data = json.loads(f.read())
        black_cards += data['blackCards']
        white_cards += data['whiteCards'] 

    return {'black_cards': black_cards, 'white_cards': white_cards}
        