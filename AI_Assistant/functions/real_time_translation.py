from flask import Blueprint
from flask import render_template
from setting import socketio
from externals.voice import Client, init_ws
from utils.login_check import check_login

real_time_translation_bp = Blueprint('real_time_translation', __name__)

client = {}

@real_time_translation_bp.route('/voice', methods=['GET'])
def voice():
    """ render html file """
    user_info = check_login()  # check which user is logged in.

    if user_info:  # if there is a logged-in user
        return render_template("voice.html", current_user=user_info.login_name)
    else:
        return render_template("voice.html")

@socketio.on('play')
def play(req):
    """ initialization of websocket """
    print(req['current_user'])
    if req['current_user'] not in client:
        client[req['current_user']]=Client()
    init_ws(client[req['current_user']], req['current_user'], req['to_lang'])

@socketio.on('update')
def update(req):
    """ send new trunk of data to third party after receiving from the front end """
    if req['current_user'] in client:
        client[req['current_user']].send(req['data'])

@socketio.on('stop')
def stop(req):
    """ stop the process, including websocket """
    print(req['current_user'])
    client[req['current_user']].stop_send()
    socketio.emit('reply', {"user": req['current_user'], "result": " \n----------------\nstopped\n----------------\n", "end": 1})