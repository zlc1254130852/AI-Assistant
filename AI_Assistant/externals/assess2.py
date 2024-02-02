# -*- coding: utf-8 -*-
# #
# #   Adapted from the demo provided by Tencent

import json
import uuid
import base64

from tencentcloud.common import credential
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.soe.v20180724 import soe_client, models
from api_key import Tencent_SecretId, Tencent_SecretKey

def send_to_assess(f,form):
    SecretId=Tencent_SecretId
    SecretKey=Tencent_SecretKey

    cred = credential.Credential(SecretId, SecretKey)

    client = soe_client.SoeClient(cred, "")

    req = models.TransmitOralProcessWithInitRequest()

    SessionId = str(uuid.uuid1())

    if type(f)==str:
        base64_data = f
    else:
        base64_data = base64.b64encode(f.read()).decode()

    params = {
        "SeqId": 1,
        "IsEnd": 1,
        "VoiceFileType": form,
        "VoiceEncodeType": 1,
        "UserVoiceData": base64_data,
        "SessionId": SessionId,
        "RefText": "",
        "WorkMode": 1,
        "EvalMode": 3,
        "ServerType": 0,
        "ScoreCoeff": 1.0
    }
    req.from_json_string(json.dumps(params))
    try:

        resp = client.TransmitOralProcessWithInit(req)

        return resp.to_json_string()

    except TencentCloudSDKException as err:
        return err

