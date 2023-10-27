from flask import request, make_response
from functools import wraps
import jwt
import os
import re

class auth_model():
    def token_auth(self,func):
        @wraps(func)
        def decorated_func(*args):
            token = str(request.headers.get('Authorization'))
            if re.match("^Bearer *([^ ]+) *$",token,flags=0):
                token = token.split(' ')[1]
                try:
                    key = os.getenv("SECRET")
                    user = jwt.decode(token, key, algorithms = "HS256")
                    request.user= {"email":user['email']}
                    return func(*args)
                except Exception as e:
                    print(e)
                    return make_response({"success":False,"message":"Invalid Token"},400)
            else:
                return make_response({"success":False,"message":"Invalid Token"},400)
        return decorated_func