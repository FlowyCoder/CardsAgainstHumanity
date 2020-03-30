import eventlet
import socketio
import json
import jsonpickle
from classes.player import Player
from classes.game import Game

sio = socketio.Server()
app = socketio.WSGIApp(sio, static_files={
    '/': {'content_type': 'text/html', 'filename': 'index.html'}
})

rooms = dict()

g = Game()


@sio.event
def connect(sid, environ):
    print('connect ', sid)
    sio.emit('event', {'response': 'my response'})


@sio.event
def my_message(sid, data):
    print('message ', data)


@sio.on("player account")
def player_account(sid, data):
    print(data)
    x = Player(sid, data['name'], None, 0)
    g.players.append(x)
    sio.enter_room(sid, data['room'])
    if data['room'] in rooms:
        rooms.get(data['room']).append(sid)
    else:
        rooms[data['room']] = [sid]
    print(g.players)


@sio.on("white card")
def white_card(sid, data):
    drawed_card = g.drawWhite()
    drawed_card_json = "{'name': '" + drawed_card + "'}"
    print(drawed_card_json)
    # sio.send(drawed_card_json, sid)
    sio.emit('white card', drawed_card_json, room=sid)


# Should be sended by group host (first one joined)
@sio.on('black card')
def black_card(sid, data):
    drawed_card = g.drawBlack()
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
