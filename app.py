import eventlet
import jsonpickle
import socketio
import json

from classes import player
from classes.player import Player
from classes.game import Game
from classes.house import House

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

    return {'players': list(map(lambda p: {'name': p.name}, game.players)), 'zar': game.zar}


@sio.on("start_game")
def start_game(sid):
    game = house.get_game_of_player(sid)
    if not game:
        return {'error': 'You are not in a lobby'}

    if game.host != sid:
        return {'error' : 'You are not the host'}

    game.draw_player_hands()
    black = game.draw_black()

    players = game.players
    for player in players:
        print("send: ", player.name, " ", player.hand)
        sio.emit('game_start', {'hand': player.hand, 'black': black}, to=player.sid)

@sio.on("place_cards")
def place_cards(sid, cards):
    game = house.get_game_of_player(sid)
    game.player_placed(sid, cards)
    player = game.get_player(sid)
    print("Room: ", game.name, " Player: ", player.name, " rooms: ", sio.rooms)

    sio.emit('cards_placed', player.name, room=game.name)


@sio.on("reveal")
def reveal_cards(sid, data):  # in data pos of the revealed card
    room = str(get_room(games, sid))
    game = games[room]
    zar = game.players[game.zar]  # Actual zar

    if zar.id == sid:
        sio.emit("cards_revealed", game.placed_cards[data['pos']], room=room)


@sio.on("winner_selected")
def winner(sid, data):
    room = str(get_room(games, sid))
    game = games[room]

    if game.players[game.zar].id == sid:
        player_won = game.players[jsonpickle.decode(data['pos'], classes=player)]
        new_zar = game.new_zar()

        sio.emit('winner', "{'player' : '" + jsonpickle.decode(player_won) + "', 'zar' : '" + new_zar + "'}", room=room)


@sio.on("white_card")
def white_card(sid, data):
    room = str(get_room(games, sid))
    print(room + " hi")
    drawed_card = games[room].drawWhite()
    drawed_card_json = "{'name': '" + drawed_card + "'}"
    print(drawed_card_json)
    # sio.send(drawed_card_json, sid)
    sio.emit('white card', drawed_card_json, room=sid)
    for x in games[room].players:
        if x.id == sid:
            x.hand.append(drawed_card)
            break


# Should be sended by group host (first one joined)
@sio.on('black_card')
def black_card(sid, data):
    room = get_room(games, sid)
    drawed_card = games[room].drawBlack()
    drawed_card_json = jsonpickle.encode(drawed_card)
    print(drawed_card_json)
    for key, value in rooms.items():
        if sid in value:
            sio.emit('black card', drawed_card_json, room=key)
            break


# TODO maybe save won black card in player class
@sio.on("points")
def points(sid, data):
    g.addPoint(sid)


@sio.event
def disconnect(sid):
    for game in house.games.values():
        if(game.has_player(sid)):
            sio.leave_room(sid, game.name)
            player = game.remove_player(sid)
            sio.emit('player_leave', player.name, game.name)
    print('disconnect ', sid)


if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 5000)), app)
