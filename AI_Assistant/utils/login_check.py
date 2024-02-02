# -*- coding:utf-8 -*-
# #
# #   Check cookies for logged-in user info

from flask import request
import hashlib
from tables import User

def check_login():
    """ check cookies for the login info"""
    cookies = request.cookies
    cookie_name = "Assistant"
    auth_cookie = cookies[cookie_name] if cookie_name in cookies else None
    if auth_cookie is None:
        return False

    auth_info = auth_cookie.split("#") # cookie format: id#encryted_user_info
    if len(auth_info) != 2:
        return False

    try:
        user_info = User.query.filter_by(id=auth_info[0]).first()
    except Exception:
        return False

    if user_info is None:
        return False

    m = hashlib.md5()
    str = "%s-%s" % (user_info.login_pwd,user_info.login_salt)
    m.update(str.encode("utf-8"))

    # check if cookie info matched with saved user info
    if auth_info[1] != m.hexdigest():
        return False

    return user_info