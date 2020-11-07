import eventlet
import socketio

sio = socketio.Server()
app = socketio.WSGIApp(sio)


@sio.event
def connect(sid, environ):  # connection establishing
    print('connect ', sid)
    pass


@sio.event
def my_message(sid, data):  # receiving data
    print(data)
    global data1
    data1 = data
    # print(data1)


@sio.event
def disconnect(sid):
    print('disconnect ', sid)


if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 5100)), app)  # add IP address
