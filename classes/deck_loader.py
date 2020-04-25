import json

def load_decks(decks, lang):
    black_cards = []
    white_cards = []

    for deck in decks:
        f = open("../decks/{0}/{1}.txt".format(lang, deck), "r")
        data = json.loads(f.read())
        black_cards += data['blackCards']
        white_cards += data['whiteCards'] 

    return {'black_cards': black_cards, 'white_cards': white_cards}
        