from flask import Blueprint
from flask import render_template
from setting import socketio
from utils.transform import pcm2wav
from externals.assess import send_assess
from utils.login_check import check_login

oral_assessment_bp = Blueprint('oral_assessment', __name__)

file = {}
text = {}

@oral_assessment_bp.route('/assess', methods=['GET'])
def assess():
    """ render html file """
    user_info = check_login()  # check which user is logged in.

    if user_info:  # if there is a logged-in user
        return render_template("assess.html", current_user=user_info.login_name)
    else:
        return render_template("assess.html")

@socketio.on('play2')
def play2(req):
    """ initialization of file to write data into"""
    if req['current_user'] not in file:
        file[req['current_user']]=open("static/en/example"+req['current_user']+".pcm", "wb")

    if req['current_user'] not in text:
        text[req['current_user']] = req['text']

@socketio.on('update2')
def update2(req):
    """ process trunked audio data """
    if req['current_user'] not in file:
        return

    if 'stop' in req:
        file_popped=file.pop(req['current_user'])
        file_popped.close()

        file_path = r"static/en/example"+req['current_user']+".pcm"
        to_path = r"static/en/example"+req['current_user']+".wav"
        pcm2wav(file_path, to_path)
        message=send_assess(text[req['current_user']],req['current_user'])
        text.pop(req['current_user'])
        socketio.emit('reply2', {"user": req['current_user'], "result": " "+message, "end": 1})

    else:
        file[req['current_user']].write(req['data'])