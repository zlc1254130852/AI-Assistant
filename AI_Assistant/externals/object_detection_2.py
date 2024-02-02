# -*- coding: utf-8 -*-
# #
# #   Adapted from the demo provided by Tencent

import json
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.tiia.v20190529 import tiia_client, models
from api_key import Tencent_SecretId, Tencent_SecretKey

def obj_detection(imageData):
    try:
        cred = credential.Credential(Tencent_SecretId, Tencent_SecretKey)

        httpProfile = HttpProfile()
        httpProfile.endpoint = "tiia.tencentcloudapi.com"

        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile

        client = tiia_client.TiiaClient(cred, "ap-shanghai", clientProfile)

        req = models.DetectLabelProRequest()
        params = {'ImageBase64':imageData}
        req.from_json_string(json.dumps(params))

        resp = client.DetectLabelPro(req)

        print(resp.to_json_string())
        return resp.to_json_string()

    except TencentCloudSDKException as err:
        print(err)
        return err
