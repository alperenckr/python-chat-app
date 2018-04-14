#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Linggar Primahastoko
# Email: x@linggar.asia

from flask import Flask, render_template, session, request, redirect,  url_for
from flask_socketio import SocketIO, Namespace, emit, disconnect, join_room, rooms, leave_room, close_room

async_mode = None

app = Flask(__name__, static_url_path='/static')
app.config['SECRET_KEY'] = "s3cr3t!"

socketio = SocketIO(app, async_mode=async_mode)
clients = []
users = {}
all_chat = {}

thread = None
def background_thread():
	count = 0
	while True:
		socketio.sleep(10)
		count += 1

def get_username(sid):
	for user in users:
		if users[user] == sid:
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
		users[message['user']] = request.sid
		all_chat[message['user']] = []
		emit('user_response', {
				'type': 'connect',
				'message': '{0} is connected to the server'.format(message['user']),
				'data': {
					'users': users
				},
			}, broadcast=True)

	def on_private_message(self, message):
		user = get_username(request.sid)
		if message['user'] not in all_chat[user]:
			emit('message_response', {
					'type': 'private',
					'message': '',
					'data': {
						'user': message['user'],
					},
				})
			all_chat[user].append(message['user'])	

	def on_my_ping(self):
		emit('my_pong')

socketio.on_namespace(WebChat('/chat'))

if __name__ == '__main__':
	socketio.run(app, debug=True, port=80)