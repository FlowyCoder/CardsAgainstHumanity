import json
import random
from player import Player
from cards import BlackCard, WhiteCard
from typing import List

import requests

class Game:

    def __init__(self, game):

        self.status = False
        self._players: List[Player] = []
        self.middle_deck = []
        self.host = None
        self.card_deck = ""
        self.placed_cards = []
        self.zar = 0
        self.room = room
        self.hand_size = 7

        # Load Json from CaH Json Website
        self.card_deck = "Base"
        payload = {"'decks[]': '" + self.card_deck + "', 'type': 'JSON'"}
        r = requests.post('https://crhallberg.com/cah/output.php', payload)
        black_white_deck = r.text
        o = json.loads(black_white_deck)

        # Load json into list object
        self.black_cards: list = o['blackCards']
        self.white_cards: list = o['whiteCards']
        random.shuffle(self.black_cards)
        random.shuffle(self.white_cards)

    def draw_black(self):
        return self.black_cards.pop()

    def draw_white(self, amount = 1):
        choosen_cards = self.white_cards[amount:]
        del self.white_cards[amount:]
        return choosen_card

    def draw_player_hands(self):
        for player in self._players:
            player.hand = self.draw_white(self.hand_size)

    def remove_player(self, sid):
        for player in self._players:
            if player.id == sid:
                self.players.remove(player)
                break

    def addPoint(self, sid):
        for player in self._players:
            if player.sid == sid:
                player.points += 1
                break

    def get_player(self):
        return self._players

    def add_player(self, player: Player):
        if len(self._players) == 0:
            self.host = player.sid

        self._players.append(player)

    players = property(get_player, add_player)

    def new_zar(self):
        number_players = len(self._players)
        self.zar = (self.zar + 1) % number_players
        return self.zar
      
    def has_player(self, sid):
        return len(list(filter( lambda p: p.sid == sid, self._players))) > 0
