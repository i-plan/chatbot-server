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


# sio.connect('ws://flask-c8d3-42278-4-1309166807.sh.run.tcloudbase.com')
# sio.connect('https://flask-c8d3-42278-4-1309166807.sh.run.tcloudbase.com')
# sio.connect('https://chatbot-server-production-cf19.up.railway.app')
# sio.connect('wss://chatbot-server-production-cf19.up.railway.app')
# sio.connect('https://flask-c8d3-prod-1gj8r0g67f17c052-1309166807.ap-shanghai.run.wxcloudrun.com')
# sio.connect('wss://flask-c8d3-prod-1gj8r0g67f17c052-1309166807.ap-shanghai.run.wxcloudrun.com/')
sio.connect("wss://express-v4zs-prod-1gj8r0g67f17c052-1309166807.ap-shanghai.run.wxcloudrun.com")
# sio.connect('https://starstech.cloud')
sio.emit('chat', {'message': 'I am client'})
