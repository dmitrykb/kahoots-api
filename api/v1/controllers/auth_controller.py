import web
import json
from db.models import *
import http_errors


class AuthController():
    def __init__(self):
        self.user = None

    @classmethod
    def authorize(cls, f):        
        def wrapper(self, *args, **kwargs):
            if not self.find_user():
                return http_errors._401()
            return f(self, *args, **kwargs)
        return wrapper


    def find_user(self):
        # check if auth_token already exists in our database
        headers = web.ctx.env
        auth_token = web.ctx.orm.query(AuthToken).filter_by(token=headers['HTTP_AUTHTOKEN']).join(User).first()
        if auth_token and auth_token.user:
            self.user = auth_token.user
            return True
        return False