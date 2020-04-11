import json
import random

import requests


class Game:
    _players = []
    activePlayer = None
    white_card_deck = None
    black_card_deck = None
    middle_deck = []
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

        # No need for shuffle, because the cards getting choosen randomly

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
        for player in self._players:
            if player.id == sid:
                self.players.remove(player)
                break

    def addPoint(self, sid):
        for player in self._players:
            if player.id == sid:
                player.points += 1
                break


    def player(self):
        return self._players

    def add_player(self, player):
        if len(self._players) == 0:
            self.activePlayer = player

        self._players.append(player)

    players = property(player, add_player)

    def has_player(self, sid):
        return len(list(filter( lambda p: p.sid == sid, self._players))) > 0
