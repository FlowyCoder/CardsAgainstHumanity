import socketio

sio = socketio.Client()


@sio.event
def connect():
    print('connection established')
    sio.emit('player account', {'name': 'my name', 'room': 'Base'})
    sio.emit('white card', {})
    sio.emit('black card', {})


@sio.event
def my_message(data):
    print('message received with ', data)
    sio.emit('my response', {'response': 'my response'})


@sio.on("event")
def anEv(data):
    print("got it")


@sio.on("white card")
def white_card(data):
    print("White Card")
    print(data)


@sio.on("black card")
def black_card(data):
    print("Black Card")
    print(data)


@sio.event
def disconnect():
    print('disconnected from server')


sio.connect('http://217.160.171.237:80/')
sio.wait()
