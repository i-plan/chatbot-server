import time

import socketio

num = 1

sio = socketio.Client()


@sio.on('chat')
def on_message(data):
    global num
    print(f'第{num}次发送')
    num += 1
    time.sleep(1)
    print('client received a message!', data)
    sio.emit('server', {'message': 'who are you', 'session_id': ''})


@sio.event
def connect_error(info):
    print(f"The connection failed: {info}")


@sio.event
def disconnect():
    print('disconnected from server')


sio.connect('http://localhost:9000')
sio.emit('chat', {'message': 'I am client'})
