<<<<<<< HEAD
from flask import Flask, render_template, request
from flask_socketio import SocketIO

# https://flask-socketio.readthedocs.io/en/latest/
# https://github.com/socketio/socket.io-client

app = Flask(__name__)

app.config[ 'SECRET_KEY' ] = '123456'
socketio = SocketIO(app, path = '/chat_application.io')

@app.route('/')
def hello():
    print(request.environ.get('HTTP_X_REAL_IP', request.remote_addr))
    return render_template( '/ChatApp.html' )

def messageRecived():
    print( 'message was received!!!' )

@socketio.on('connection') # Javascript içerisinde yer alan connection
def first_connection( json ):
    print( 'recived my event: ' + str( json ) )
    socketio.emit('my response', json, callback=messageRecived )
    return 

@socketio.on('message sending')
def message_received(json):
    print('received message: ', str(json))


if __name__ == '__main__':
    socketio.run(app,'127.0.0.1',80)
=======
from flask import Flask, render_template, request
from flask_socketio import SocketIO, join_room, leave_room, rooms

# https://flask-socketio.readthedocs.io/en/latest/
# https://github.com/socketio/socket.io-client

app = Flask(__name__)

app.config[ 'SECRET_KEY' ] = '123456'
socketio = SocketIO(app)

user_list = {}
user_rooms = []

@app.route('/')
def hello():
    print(request.environ.get('HTTP_X_REAL_IP', request.remote_addr))
    return render_template( '/ChatApp.html' )

@socketio.on( 'connection' )
def first_connection( json ):
    print( 'a user is connected ' + str( json ) )
    user_list[json['nick_name']] = {'ip' : request.remote_addr, 'state': True}
    user_rooms.append(json['nick_name'])
    join_room(json['nick_name'])
    socketio.emit('reset_users',data=" ")
    for it in user_rooms:
        socketio.emit('append_user',it)
    print(rooms())
    return

@socketio.on('join')
def join(json):
    print('a chat request is sond:  '+str(json))
    socketio.send('chat_request', json['nick_name'], room=json['room'])
    return

@socketio.on('permission')
def permission(json):
    if json['perm'] is True:
        send('accepted',room=json['room'])
    else:
        send('rejected', room=json['room'])




@socketio.on('message sending')
def message_received(json):
    print('received message: ', str(json))
    socketio.emit('response', json)
    return

def check_online_users():
    import time
    while True:
       for key, inf in user_list:
           inf[1] = False
       socketio.emit('check', 'hello')
       time.sleep(1)
       socketio.emit('user_states',user_list)
       time.sleep(14)


@socketio.on('logout')
def logout(data):
    user_list[data]['state'] = False

@socketio.on('online')
def mark_as_online(data):
    user_list[data]['state'] = True

if __name__ == '__main__':
    socketio.run(app,host='0.0.0.0')
    #socketio.start_background_task(check_online_users)
>>>>>>> 0e0741637c1c840df1466d75e2246b640bdd12f0
