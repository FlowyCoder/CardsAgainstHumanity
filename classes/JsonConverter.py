import json
from classes.player import Player
from classes.cards import BlackCard, WhiteCard
from classes.game import Game


def as_player(d):
    p = Player()
    p.__dict__.update(d)
    return p

def as_black_card(c):
    p = BlackCard()
    p.__dict__.update(c)
    return p

def as_white_card(c):
    p = WhiteCard()
    p.__dict__.update(c)
    return p

def as_game(g):
    p = Game()
    p.__dict__.update(g)
    return p