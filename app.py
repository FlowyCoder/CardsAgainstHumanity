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

    player = Player(sid, name)

    sio.enter_room(sid, lobby)

    game = house.get_game(lobby)
    if not game.add_player(player):
        return {'error': 'Player name already exists'}

    sio.emit('player_join', {'name': player.name}, lobby)  # Sending new player information to other players
    host = game.get_player(game.host)

    return {'players': list(map(lambda p: {'name': p.name, 'points': 0}, game.players)), 'host': host.name}


@sio.on("start_game")
def start_game(sid):
    game = house.get_game_of_player(sid)
    if not game:
        return {'error': 'You are not in a lobby'}

    if game.host != sid:
        return {'error': 'You are not the host'}

    if len(game.players) < 3:
        return {'error': 'Not enough players in the Lobby'}

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
        return {'error': 'You are not the zar'}

    if not game.all_players_placed():
        return {'error': 'Not all players have placed their cards'}

    players = list(filter(lambda p: p.sid != sid and not game.is_player_revealed(p.sid), game.players))

    if len(players) == 0:
        return {'error': 'All players are revealed'}

    player = random.choice(players)

    game.player_revealed(player.sid)
    
    sio.emit("cards_revealed", {'pos': pos, 'tempId': player.tempId, 'cards': game.placed_cards[player.sid]}, room=game.name)


@sio.on("winner_selected")
def winner(sid, tempId):
    game = house.get_game_of_player(sid)

    if game.get_zar().sid != sid:
        return {'error': 'You are not the zar'}

    if not game.all_cards_revealed():
        return {'error': 'Not all cards are revealed'}

    winning_player = game.get_player_with_tempId(tempId)

    if not winning_player:
        return {'error': 'Player with name ' + name + ' not found'}

    winning_player.points += 1

    if winning_player.points >= game.points_to_win:
        points = {}
        for player in game.players:
            points[player.name] = player.points
        sio.emit('game_end', points, room=game.name)
    else:
        game.start_round()
        for player in game.players:
            sio.emit('next_round', {'hand': player.hand, 'black': game.black_card, 'zar': game.get_zar().name, 'winner': winning_player.name}, to=player.sid)

@sio.on("points")
def points(sid, data):
    g.addPoint(sid)


@sio.event
def disconnect(sid):
    for game in house.games.values():
        if game.has_player(sid):
            sio.leave_room(sid, game.name)
            player = game.remove_player(sid)
            if len(game.players) == 0:
                del house.games[game.name]
            sio.emit('player_leave', player.name, game.name)
    print('disconnect ', sid)


if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 5000)), app)
