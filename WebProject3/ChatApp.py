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

@socketio.on( 'connection' )
def first_connection( json ):
    print( 'recived my event: ' + str( json ) )
    socketio.emit( 'my response', json, callback=messageRecived )
    return

@socketio.on('message sending')
def message_received(json):
    print('received message: ', str(json))


if __name__ == '__main__':
    socketio.run(app,'127.0.0.1',80)
