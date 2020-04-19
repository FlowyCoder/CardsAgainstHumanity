#!/usr/bin/env python3

import random

import eventlet
import socketio

from classes.house import House
from classes.player import Player

sio = socketio.Server(cors_allowed_origins='*')
app = socketio.WSGIApp(sio, static_files={
    '/': {'content_type': 'text/html', 'filename': 'index.html'}
})

house = House()


@sio.event
def connect(sid, environ):
    print('connect ', sid)
    sio.emit('event', {'response': 'my response'})


@sio.event
def my_message(sid, data):
    print('message ', data)


@sio.on("join")
def join(sid, data):
    name = data['name']
    lobby = data['lobby']

    game = house.get_game(lobby)

    if game.game_state != "Lobby":
        return {'error': 'Game already running.'}

    player = Player(sid, name)
    sio.enter_room(sid, lobby)

    if not game.add_player(player):
        return {'error': 'Player name already exists.'}

    sio.emit('player_join', {'name': player.name}, lobby)  # Sending new player information to other players
    host = game.get_player(game.host)

    return {
        'players': list(map(lambda p: {'name': p.name, 'points': 0}, game.players)),
        'host': host.name,
        'points_to_win': game.points_to_win,
        'hand_size': game.hand_size,
        'card_decks': game.card_decks
    }


@sio.on("start_game")
def start_game(sid):
    game = house.get_game_of_player(sid)
    if not game:
        return {'error': 'You are not in a lobby.'}

    if game.host != sid:
        return {'error': 'You are not the host.'}

    if len(game.players) < 3:
        return {'error': 'Not enough players in the Lobby.'}

    game.start_round()

    players = game.players
    for player in players:
        print("send: ", player.name, " ", player.hand)
        sio.emit('game_start', {'hand': player.hand, 'black': game.black_card, 'zar': game.get_zar().name}, to=player.sid)


@sio.on("place_cards")
def place_cards(sid, cards):
    game = house.get_game_of_player(sid)
    game.player_placed_cards(sid, cards)
    player = game.get_player(sid)
    print("Room: ", game.name, " Player: ", player.name, " rooms: ", sio.rooms)

    sio.emit('cards_placed', player.name, room=game.name)


@sio.on("reveal")
def reveal_cards(sid, pos):
    game = house.get_game_of_player(sid)
    zar = game.get_zar()

    if zar.sid != sid:
        return {'error': 'You are not the zar.'}

    if not game.all_players_placed():
        return {'error': 'Not all players have placed their cards.'}

    players = list(filter(lambda p: p.sid != sid and not game.is_player_revealed(p.sid), game.players))

    if len(players) == 0:
        return {'error': 'All players are revealed.'}

    player = random.choice(players)

    game.player_revealed(player.sid)
    
    sio.emit("cards_revealed", {'pos': pos, 'tempId': player.tempId, 'cards': game.placed_cards[player.sid]}, room=game.name)


@sio.on("winner_selected")
def winner(sid, tempId):
    game = house.get_game_of_player(sid)

    if game.get_zar().sid != sid:
        return {'error': 'You are not the zar.'}

    if not game.all_cards_revealed():
        return {'error': 'Not all cards are revealed.'}

    winning_player = game.get_player_with_tempId(tempId)

    if not winning_player:
        return {'error': 'Player with name ' + name + ' not found.'}

    winning_player.points += 1

    if winning_player.points >= game.points_to_win:
        game.end_game()

        points = {}
        for player in game.players:
            points[player.name] = player.points
        sio.emit('game_end', points, room=game.name)
    else:
        tempIds = {}
        for player in game.players:
            tempIds[player.tempId] = player.name

        game.start_round()
        for player in game.players:
            sio.emit('next_round', {
                'hand': player.hand,
                'black': game.black_card,
                'zar': game.get_zar().name,
                'winner': winning_player.name,
                'tempIds': tempIds
            }, to=player.sid)

@sio.on("change_settings")
def change_settings(sid, settings):
    game = house.get_game_of_player(sid)

    if game.get_zar().sid != sid:
        return {'error': 'You are not the zar.'}
    
    if game.game_state != "Lobby":
        return {'error': 'Settings can only be canged in the lobby.'}

    if settings['card_decks']:
        game.set_card_decks(settings['card_decks'])

    if settings['points_to_win']:
        game.points_to_win = settings['points_to_win']

    if settings['hand_size']:
        game.hand_size = settings['hand_size']

    sio.emit('settings_changed', settings, room=game.name)

    return {'info': 'The settings have been chnaged.'}

@sio.on("games")
def games(sid, password):
    if(password != 'Umpa Lumpas'):
        return {'error': 'Wrong password.'}

    return [game.to_json() for game in house.games.values()]

@sio.on("players")
def players(sid, password):
    if(password != 'Umpa Lumpas'):
        return {'error': 'Wrong password.'}

    return [player.to_json() for game in house.games.values() for player in game.players]


@sio.event
def disconnect(sid):
    print('disconnect ', sid)

    for game in house.games.values():
        if game.has_player(sid):
            sio.leave_room(sid, game.name)

            if len(game.players) == 1:
                del house.games[game.name]
                return

            zar = game.get_zar()
            player = game.remove_player(sid)
            sio.emit('host', game.get_player(game.host).name, game.name)
            sio.emit('player_leave', player.name, game.name)
                
            if len(game.players) < 3:
                game.end_game()
                points = {}
                for player in game.players:
                    points[player.name] = player.points
                    sio.emit('game_end', points, room=game.name)
            elif player == zar:
                game.start_round()
                for player in game.players:
                    sio.emit('next_round', {
                        'hand': player.hand,
                        'black': game.black_card,
                        'zar': game.get_zar().name,
                        'winner': ''
                    }, to=player.sid)




if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.wrap_ssl(eventlet.listen(('', 5000)), certfile='cert.crt', keyfile='private.key', server_side=True), app)
