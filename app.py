import eventlet
import jsonpickle
import socketio

from classes import player
from classes.game import Game
from classes.helperFunctions import get_room
from classes.player import Player

sio = socketio.Server(cors_allowed_origins='*')
app = socketio.WSGIApp(sio, static_files={
    '/': {'content_type': 'text/html', 'filename': 'index.html'}
})

rooms = dict()
games = dict()


@sio.event
def connect(sid, environ):
    print('connect ', sid)
    sio.emit('event', {'response': 'my response'})


@sio.event
def my_message(sid, data):
    print('message ', data)


@sio.on("player_account")
def player_account(sid, data):
    print(data)
    x = Player(sid, data['name'], None, 0)
    sio.enter_room(sid, data['room'])
    if data['room'] in rooms:
        rooms.get(data['room']).append(sid)
    else:
        rooms[data['room']] = [sid]
        games[data['room']] = Game(data['room'])
        games[data['room']].host = sid

    games[data['room']].players.append(x)
    sio.emit('new player', x.get_json(), data['room'])  # Sending new player information to other players
    print(games)
    # create_and_send_deck(sid, room)
    return list(map(lambda p: p.get_json(), games[data['room']].players))


@sio.on("game_start")
def game_start(sid):
    room = str(get_room(games, sid))
    if games[room].host == sid:
        game_starting(sid, room)
    else:
        return "{'response' : 'you are not the host'}"


def game_starting(sid, room):  # TODO time limit for one turn
    players = games[room].players
    amount_cards = 7
    for player in players:  # Everyone gets 7 cards
        deck = []
        for i in range(1, amount_cards):
            deck.append(games[room].drawWhite())
        player.hand = deck
        sio.send('game start', jsonpickle.encode(deck), player.id)

    sio.emit(games[room].drawBlack(), room=sid)


@sio.on("place_card")
def place_card(sid, data):
    room = str(get_room(games, sid))
    game = games[room]
    players = game.players
    card = data['text']

    for x in players:
        if x.sid == sid:
            for c in x.hand:
                if c.text == card:
                    game.placed_cards.append(c)
                    x.hand.remove(c)
                    break


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
    sio.leave_room(sid)
    g.removePlayer(sid)
    print('disconnect ', sid)


if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 5000)), app)
