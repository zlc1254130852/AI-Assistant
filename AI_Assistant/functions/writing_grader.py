from flask import Blueprint
from flask import render_template
from flask import request, Response
import json
from api_key import DIFY_API_KEY_WRITING
import requests
from utils.stream_generation import generate_dify_writing
from utils.login_check import check_login

writing_grader_bp = Blueprint('writing_grader_translation', __name__)

@writing_grader_bp.route('/chat2', methods=['GET'])
def chat2():
    """ render html file """
    user_info = check_login()  # check which user is logged in.

    if user_info:  # if there is a logged-in user
        return render_template("chat2.html", current_user=user_info.login_name)
    else:
        return render_template("chat2.html")

@writing_grader_bp.route('/chat2', methods=['POST'])
def answer2():
    """ send to DIFY for further assessment """
    headers = {'Authorization': DIFY_API_KEY_WRITING, 'Content-Type': 'application/json'}
    payload = {'inputs': {}, 'query': request.json["query"], 'response_mode': 'streaming', 'conversation_id': '', 'user': request.json["current_user"]}

    response = requests.post("https://api.dify.ai/v1/chat-messages", data=json.dumps(payload), headers=headers)

    headers = {
        'Content-Type': 'text/event-stream',
        'Cache-Control': 'no-cache',
        'X-Accel-Buffering': 'no'
    }

    return Response(generate_dify_writing(response), mimetype="text/event-stream", headers=headers)