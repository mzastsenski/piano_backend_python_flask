from flask import request, make_response
from __main__ import app
import jwt
from functools import wraps
from decouple import config
import logging
logging.basicConfig(level=logging.DEBUG)


def check_token():
    def _check_token(f):
        @wraps(f)
        def __check_token(*args, **kwargs):
            cookie_token = request.cookies.get("token")
            secret = config('ACCESS_TOKEN_SECRET')
            if cookie_token:
                try:
                    jwt.decode(cookie_token, secret, algorithms=['HS256'])
                    return f(*args, **kwargs)
                except:
                    return make_response("401", 401)
            else:
                return make_response("401", 401)
        return __check_token
    return _check_token

