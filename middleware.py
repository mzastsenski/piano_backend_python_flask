from flask import request, make_response
import jwt
from decouple import config
from functools import wraps


def check_token():
    def _check_token(f):
        @wraps(f)
        def __check_token(*args, **kwargs):
            cookie_token = request.cookies.get("token")
            secret = uri = config('ACCESS_TOKEN_SECRET')
            if cookie_token:
                try:
                    jwt.decode(cookie_token, 'secret', algorithms=['HS256'])
                    return f(*args, **kwargs)
                except:
                    return make_response("401", 401)
            else:
                return make_response("401", 401)
        return __check_token
    return _check_token

