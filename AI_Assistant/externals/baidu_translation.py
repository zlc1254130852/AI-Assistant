# -*- coding:utf-8 -*-
# #
# #   Adapted from the demo provided by Baidu

import random
import requests
from hashlib import md5
from api_key import BAIDU_TRANSLATION_APPID, BAIDU_TRANSLATION_APPKEY

# Set your own appid/appkey.

appid = BAIDU_TRANSLATION_APPID
appkey = BAIDU_TRANSLATION_APPKEY

# For list of language codes, please refer to `https://api.fanyi.baidu.com/doc/21`
from_lang = 'en'
to_lang =  'zh'

endpoint = 'http://api.fanyi.baidu.com'
path = '/api/trans/vip/translate'
url = endpoint + path

# Generate salt and sign
def make_md5(s, encoding='utf-8'):
    return md5(s.encode(encoding)).hexdigest()

def baidu_translate(source_text, target_lang=to_lang, from_lang=from_lang):
    salt = random.randint(32768, 65536)
    # Build request
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    sign = make_md5(appid + source_text + str(salt) + appkey)
    payload = {'appid': appid, 'q': source_text, 'from': from_lang, 'to': target_lang, 'salt': salt, 'sign': sign}
    r = requests.post(url, params=payload, headers=headers)
    result = r.json()
    if "trans_result" in result:
        return result["trans_result"][0]["dst"]
    else:
        return ""