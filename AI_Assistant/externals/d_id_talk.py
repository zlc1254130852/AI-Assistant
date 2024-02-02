# -*- coding:utf-8 -*-
# #
# #   Adapted from the demo provided by D-ID

import requests
import time,json
from api_key import D_ID_TALK_API_KEY

def generate_video(input):
    url = "https://api.d-id.com/talks"

    payload = {
        "script": {
            "type": "text",
            "subtitles": "false",
            "provider": {
                "type": "microsoft",
                "voice_id": "en-US-JennyNeural"
            },
            "ssml": "false",
            "input": input
        },
        "config": {
            "fluent": "false",
            "pad_audio": "0.0"
        },
        "source_url": "https://cdn.broadbandtvnews.com/wp-content/uploads/2019/02/14113059/Xin-Xiaomeng.jpeg"
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": D_ID_TALK_API_KEY
    }

    response = requests.post(url, json=payload, headers=headers)

    print(response.text)

    url2 = "https://api.d-id.com/talks/"+response.json()['id']

    headers2 = {
        "accept": "application/json",
        "authorization": D_ID_TALK_API_KEY
    }

    while True:
        time.sleep(0.333)
        print("waiting")
        response2 = requests.get(url2, headers=headers2)
        print(response2.text)
        if 'result_url' in json.loads(response2.text):
            return response2.json()['result_url']