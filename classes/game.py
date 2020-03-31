import json
import random

import requests


class Game:
    players = []
    white_card_deck = None
    black_card_deck = None
    room = None

    def __init__(self, room):

        # Load Json from CaH Json Website
        payload = {'decks[]': 'Base', 'type': 'JSON'}
        r = requests.post('https://crhallberg.com/cah/output.php', payload)
        black_white_deck = r.text
        o = json.loads(black_white_deck)

        # Load json into list object
        self.black_card_deck = o['blackCards']
        self.white_card_deck = o['whiteCards']
        print(self.black_card_deck)

        # Random ordered list
        random.shuffle(self.black_card_deck)
        # Base pack 460
        # TODO another deck for already used cards to later shuffle in
        random.shuffle(self.white_card_deck)

        self.room = room

    def drawBlack(self):
        choosen_card = random.choice(self.black_card_deck)
        self.black_card_deck.remove(choosen_card)
        return choosen_card

    def drawWhite(self):
        choosen_card = random.choice(self.white_card_deck)
        self.white_card_deck.remove(choosen_card)
        return choosen_card

    def removePlayer(self, sid):
        for player in self.players:
            if player.id == sid:
                self.players.remove(player)
                break

    def addPoint(self, sid):
        for player in self.players:
            if player.id == sid:
                player.points += 1
                break
