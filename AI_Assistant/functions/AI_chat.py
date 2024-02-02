# -*- encoding:utf-8 -*-
from flask import Blueprint
from flask import render_template
from flask import request, Response
from utils.login_check import check_login

from pydub import AudioSegment
import scipy.io.wavfile as wav
from utils.stream_generation import generate_AI_chat, generate_bwav
from tables import Message
from setting import db
import json

AI_chat_bp = Blueprint('AI_chat', __name__)

openai_client = {}

ctrler = {}

@AI_chat_bp.route('/chat', methods=['GET'])
def chat():
    """ render html file """
    user_info = check_login()  # check which user is logged in.

    if user_info:  # if there is a logged-in user
        return render_template("chat.html", current_user=user_info.login_name)
    else:
        return render_template("chat.html")

@AI_chat_bp.route('/chat', methods=['POST'])
def answer():
    """ respond to question from the user """
    current_user=request.json["current_user"]
    if current_user not in ctrler:
        ctrler[current_user]=[1,1]
    opt=request.json["option"]
    ctrler[current_user][opt]=0
    history=eval(request.json["history"])

    model_message = Message()
    model_message.user_name = request.json["current_user"]
    model_message.app_type = request.json["app_type"]
    model_message.message_id = str(request.json["message_id"])
    model_message.content = str({"role": "user", "content": request.json["question"]})
    # model_message.created_time = datetime.datetime.now()
    db.session.add(model_message)
    db.session.commit()

    response = openai_client[current_user].chat.completions.create(
        model='gpt-3.5-turbo',
        messages=[{"role":"system","content":request.json["system"]}]+history[:-1]+[{"role":"user","content":request.json["question"]}],
        stream=True
    )

    headers = {
        'Content-Type': 'text/event-stream',
        'Cache-Control': 'no-cache',
        'X-Accel-Buffering': 'no'
    }
    # generate stream response
    return Response(generate_AI_chat(current_user,request.json["app_type"],request.json["message_id"],ctrler[current_user],opt,response), mimetype="text/event-stream", headers=headers)

@AI_chat_bp.route('/abort', methods=['POST'])
def abort():
    """ stop generating stream response at the backend """
    req = request.values
    current_user=req["current_user"]
    opt = req["option"]
    ctrler[current_user][int(opt)]=1
    return ""

@AI_chat_bp.route('/del_msg', methods=['POST'])
def del_msg():
    """ delete one chat message """
    req = request.values
    msg_user_name = req['user_name']
    msg_app_type = req['app_type']
    msg_message_id = req['message_id']

    # delete message in the database
    message_info = Message.query.filter_by(user_name=msg_user_name,app_type=msg_app_type,message_id=msg_message_id).first()
    db.session.delete(message_info)
    db.session.commit()

    return {}

@AI_chat_bp.route('/del_all', methods=['POST'])
def del_all():
    """ clear the chat history """
    req = request.values
    msg_user_name = req['user_name']
    msg_app_type = req['app_type']

    # delete all messages in the database
    db.session.query(Message).filter(Message.user_name==msg_user_name,Message.app_type==msg_app_type).delete()
    db.session.commit()

    return {}

@AI_chat_bp.route('/load_msg', methods=['POST'])
def load_msg():
    """ when starting the application, load chat history from the database """
    msg_user_name = request.json["current_user"]
    msg_app_type = request.json["app_type"]
    history = Message.query.filter_by(user_name=msg_user_name,app_type=msg_app_type)  # getting chat history

    def generate(): # return chat messages one by one
        for i in history:
            msg_obj=eval(i.content)
            print(msg_obj)
            yield json.dumps({"msg_id":i.message_id,"msg_sender":msg_obj["role"],"msg_content":msg_obj["content"]})+"\n"

    headers = {
        'Content-Type': 'text/event-stream',
        'Cache-Control': 'no-cache',
        'X-Accel-Buffering': 'no'
    }

    return Response(generate(), mimetype="text/event-stream", headers=headers)

@AI_chat_bp.route('/translator', methods=['GET'])
def translator():
    """ render html file """
    user_info = check_login()  # check which user is logged in.

    if user_info:  # if there is a logged-in user
        return render_template("translator.html", current_user=user_info.login_name)
    else:
        return render_template("translator.html")

@AI_chat_bp.route('/play4', methods=['POST'])
def play4():
    """ text-to-speech
    for speech-to-text, please refer to play3() and update3() in speaking_grader.py """

    print(request.json["msg"])
    speech_file_path = "static/en/e4xample"+request.json["current_user"]+".mp3"
    response = openai_client[request.json["current_user"]].audio.speech.create(
        model="tts-1",
        voice=request.json["opt"].lower(),
        input=request.json["msg"]
    )
    print("response done")
    response.stream_to_file(speech_file_path)
    sound = AudioSegment.from_mp3(speech_file_path)
    sound.export("static/en/e4xample"+request.json["current_user"]+".wav", format="wav")
    rt, wavsignal = wav.read('static/en/e4xample'+request.json["current_user"]+'.wav')

    bwav=bytes(wavsignal)

    headers = {
        'Content-Type': 'text/event-stream',
        'Cache-Control': 'no-cache',
        'X-Accel-Buffering': 'no'
    }

    return Response(generate_bwav(bwav), mimetype="text/event-stream", headers=headers)