import socketio

sio = socketio.Client()


@sio.event
def connect():
    print('connection established')
    sio.start_background_task(send_data)


def send_data():
    while True:
        sio.emit('my_message', 1)
        sio.sleep(1)


@sio.event
def disconnect():
    print('disconnected from server')


sio.connect('http://localhost:5100')  # add IP address
# sio.wait()
