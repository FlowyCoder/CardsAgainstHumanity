import eventlet
import jsonpickle
import socketio
import json

from classes.game import Game
from classes.helperFunctions import get_room
from classes.player import Player

sio = socketio.Server(cors_allowed_origins='*')
app = socketio.WSGIApp(sio, static_files={
    '/': {'content_type': 'text/html', 'filename': 'index.html'}
})

games = dict()

@sio.event
def connect(sid, environ):
    print('connect ', sid)
    sio.emit('event', {'response': 'my response'})


@sio.event
def my_message(sid, data):
    print('message ', data)


@sio.on("join")
def join(sid, data):
    [name, room] = data
    player = Player(sid, data['name'], None, 0)

    sio.enter_room(sid, room)

    if room not in games:
        games[room] = Game(room)

    games[room].players.append(player)
    sio.emit('player_join', jsonpickle.encode(player), room)  # Sending new player information to other players
    print(games)
    # create_and_send_deck(sid, room)
    return json.loads(jsonpickle.encode(games[room].players))


@sio.on("white card")
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
@sio.on('black card')
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
