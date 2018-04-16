from flask import Flask, render_template, session, request, redirect,  url_for
from flask_socketio import *

async_mode = None

app = Flask(__name__, static_url_path='/static')
app.config['SECRET_KEY'] = "s3cr3t!"

socketio = SocketIO(app, async_mode=async_mode)
users = {}
clients = []
rooms = []
thread = None
def background_thread():
	count = 0
	while True:
		socketio.sleep(10)
		count += 1

def get_username(sid):
	for user in users:
		if users[user]["sid"] == sid:
			return user
	return False

@app.route('/')
def index():
	exists = request.args.get('exists', 0)
	return render_template('index.html', exists=exists)

@app.route('/check/<string:username>')
def user_check(username):
	# Kullanıcı ismi var mı diye kontrol eder
	if username in users:
		return '1'
	return '0'

@app.route('/<string:username>')
def main_chat(username):
	return render_template('chat.html', async_mode=socketio.async_mode)

class WebChat(Namespace):
	def on_connect(self):
		global thread
		clients.append(request.sid)
		if thread is None:
			thread = socketio.start_background_task(target=background_thread)

	def on_register(self, message):
		users[message['user']] = {'sid': request.sid, 'ip': request.remote_addr, 'state':True}
		emit('user_response', {
				'type': 'connect',
				'message': '{0} is connected to the server'.format(message['user']),
				'data': {
					'users': users
				},
			}, broadcast=True)

	def on_private_message_request(self, message):
		if message['user']+message['me'] not in rooms and message['me']+message['user'] not in rooms:
			join_room(message['me']+message['user'])
			emit('chat_request',message['me'],room=users[message['user']]['sid'])
		else:
			emit('already allowed', message, room=request.sid)

	def on_permission(self,message):
		if message['perm'] is True:
			join_room(message['user']+message['me'])
			rooms.append(message['user']+message['me'])
			emit('allowed', { 'user': message['me'], 'room': message['user']+message['me']},room=users[message['user']]['sid'])

	def on_sendmessage(self,message):
		print("asdasdasdasdasd")
		emit('take_message', message, room=message['me']+message['user'])
		if message['me']+message['user'] not in rooms:
			emit('take_message', message, room=message['user']+message['me'])




	def on_message(self,message):
		print(message)

	def on_my_ping(self):
		emit('my_pong')

socketio.on_namespace(WebChat('/chat'))

if __name__ == '__main__':
	socketio.run(app, debug=True, port=5000)
