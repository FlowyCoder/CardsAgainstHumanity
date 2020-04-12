import json
import random
from typing import List

import requests

from .player import Player


class Game:

    def __init__(self, name):

        self.status = False
        self.players: List[Player] = []
        self.middle_deck = []
        self.host = None
        self.card_deck = "Base"
        self.placed_cards = []
        self.zar = 0
        self.name = name
        self.hand_size = 7

        # Load Json from CaH Json Website
        payload = {'decks': self.card_deck, 'type': 'JSON'}
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
        for player in self.players:
            player.hand = self.draw_white(self.hand_size)

    def addPoint(self, sid):
        for player in self.players:
            if player.sid == sid:
                player.points += 1
                break
    
    def remove_player(self, sid):
        for player in self.players:
            if player.sid == sid:
                self.players.remove(player)
                return player

    def add_player(self, player: Player):
        print("playername: ", player.name, self.has_player_with_name(player.name), self.players)
        if self.has_player_with_name(player.name):
            return False
        if len(self.players) == 0:
            self.host = player.sid

        if not self.has_player(player.sid):
            self.players.append(player)
        return True

    def next_zar(self):
        number_players = len(self.players)
        self.zar = (self.zar + 1) % number_players
        return self.zar
      
    def has_player(self, sid):
        return len(list(filter( lambda p: p.sid == sid, self.players))) > 0

    def has_player_with_name(self, name):
        return len(list(filter( lambda p: p.name == name, self.players))) > 0
