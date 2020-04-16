import json
import random
from typing import List

import requests

from .player import Player


class Game:

    def __init__(self, name):

        self.game_state = "Lobby" # Lobby / Game
        self.players: List[Player] = []
        self.host = None
        self.card_decks = []
        self.placed_cards = {}
        self.revealed_players = []
        self.black_card = None
        self.zar = 0
        self.name = name
        self.hand_size = 7
        self.points_to_win = 5
        self.set_card_decks(["Base"])

    def set_card_decks(self, card_decks):
        self.card_decks = card_decks

        payload = {'decks[]': self.card_decks, 'type': 'JSON'}
        r = requests.post('https://crhallberg.com/cah/output.php', payload)
        black_white_deck = r.text
        o = json.loads(black_white_deck)

        # Load json into list object
        self.black_cards: list = o['blackCards']
        self.white_cards: list = o['whiteCards']
        random.shuffle(self.black_cards)
        random.shuffle(self.white_cards)

    def draw_black(self):
        self.black_card = self.black_cards.pop()

    def draw_white(self, amount = 1):
        choosen_cards = self.white_cards[:amount]
        del self.white_cards[:amount]
        return choosen_cards

    def start_round(self):
        self.game_state = "Game"
        self.draw_black()
        randIds = list(range(len(self.players)))
        random.shuffle(randIds)
        self.next_zar()
        self.revealed_players = []
        self.placed_cards = {}

        for player in self.players:
            print(player.name, " hand: ", player.hand)
            player.points = 0
            player.hand += self.draw_white(self.hand_size - len(player.hand))
            player.tempId = randIds.pop()
            
    def addPoint(self, sid):
        for player in self.players:
            if player.sid == sid:
                player.points += 1
                break

    def end_game(self):
        self.game_state = "Lobby"
        self.placed_cards = {}
        self.revealed_players = []
        self.black_card = None
        self.zar = 0

    def get_player(self, sid) -> Player:
        return next(filter(lambda p: p.sid == sid, self.players), None)

    def get_player_with_name(self, name) -> Player:
        return next(filter(lambda p: p.name == name, self.players), None)
    
    def get_player_with_tempId(self, tempId) -> Player:
        return next(filter(lambda p: p.tempId == tempId, self.players), None)
    
    def remove_player(self, sid):
        player = self.get_player(sid)
        if player:
            self.players.remove(player)
            if self.host == player.sid:
                self.host = self.players[0].sid
        return player

    def add_player(self, player: Player):
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

    def player_placed_cards(self, sid, cards):
        self.placed_cards[sid] = cards
        player = self.get_player(sid)
        for card in cards:
            if(card in player.hand):
                self.white_cards.append(card)
                player.hand.remove(card)

    def all_players_placed(self):
        return len(self.players) - 1 == len(self.placed_cards)

    def all_cards_revealed(self):
        return len(self.players) - 1 == len(self.revealed_players)

    def player_won_game(self):
        for player in self.players:
            if player.points >= self.points_to_win:
                return player
        return None

    def get_zar(self) -> Player:
        return self.players[self.zar]
    
    def player_revealed(self, sid):
        self.revealed_players.append(sid)
    
    def is_player_revealed(self, sid):
        return sid in self.revealed_players