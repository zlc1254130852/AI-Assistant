# -*- coding:utf-8 -*-
# #
# #   Adapted from the demo provided by IFlyTech

from setting import socketio
import websocket
from externals.baidu_translation import baidu_translate
import hashlib
import hmac
import base64
import json, time, threading
from websocket import create_connection
from urllib.parse import quote
from api_key import IFLY_REAL_TIME_TRANSCRITION_API_ID, IFLY_REAL_TIME_TRANSCRITION_API_KEY

app_id = IFLY_REAL_TIME_TRANSCRITION_API_ID
api_key = IFLY_REAL_TIME_TRANSCRITION_API_KEY

def init_ws(client,user,target):
    client.ws = init_real_time_translation_param(client, user, target)
    client.ws.settimeout(60)
    client.trecv = threading.Thread(target=client.recv)
    client.trecv.start()

def init_real_time_translation_param(client, user, target_lang):
    base_url = "ws://rtasr.xfyun.cn/v1/ws"
    ts = str(int(time.time()))
    tt = (app_id + ts).encode('utf-8')
    md5 = hashlib.md5()
    md5.update(tt)
    baseString = md5.hexdigest()
    baseString = bytes(baseString, encoding='utf-8')

    apiKey = api_key.encode('utf-8')
    signa = hmac.new(apiKey, baseString, hashlib.sha1).digest()
    signa = base64.b64encode(signa)
    signa = str(signa, 'utf-8')
    client.end_tag = "{\"end\": true}"
    client.to_lang = target_lang
    client.user=user

    return create_connection(base_url + "?appid=" + app_id + "&ts=" + ts + "&user=" + user + "&signa=" + quote(signa) + "&lang=en")

class Client():
    def __init__(self):
        self.to_lang="zh"
        self.end_tag = "{\"end\": true}"
        self.user=""

    def send(self, data):
        self.ws.send(data)
        time.sleep(0.04)

    def stop_send(self):
        self.ws.send(bytes(self.end_tag.encode('utf-8')))
        print("send end tag success")

    def recv(self):
        try:
            while self.ws.connected:
                result = str(self.ws.recv())
                if len(result) == 0:
                    print("receive result end")
                    self.ws.close()
                    print("connection closed")
                    break
                result_dict = json.loads(result)

                if result_dict["action"] == "started":
                    print("handshake success, result: " + result)
                    socketio.emit('reply', {"user": self.user, "result": " \n----------------\nconnected\n----------------\n", "end": 1})

                if result_dict["action"] == "result":
                    result_1 = result_dict
                    result_2 = json.loads(result_1["data"])
                    result_3 = ""
                    end_tag = ""
                    end=len(result_2["cn"]["st"]["rt"][0]["ws"])
                    result_4=result_2["cn"]["st"]["rt"][0]["ws"]
                    for i in range(0,end):
                        result_3 += result_4[i]["cw"][0]["w"]
                    end_tag = result_2["cn"]["st"]["ed"]

                    if end_tag == "0":
                        socketio.emit('reply', {"user": self.user, "result": result_3, "end": 0})

                    else:
                        socketio.emit('reply',{"user": self.user, "result":result_3,"end":1})

                        if result_3 and result_3[0] in [',','.','?','!']:
                            if len(result_3)>1:
                                result_3=result_3[1:len(result_3)]
                            else:
                                result_3=" "

                        result_5 = baidu_translate(result_3, self.to_lang)
                        socketio.emit('reply', {"user": self.user, "result": " " + result_5,"end":1})

                if result_dict["action"] == "error":
                    print("rtasr error: " + result)
                    self.ws.close()
                    return

        except websocket.WebSocketConnectionClosedException:
            print("receive result end")

    def close(self):
        self.ws.close()
        print("connection closed")