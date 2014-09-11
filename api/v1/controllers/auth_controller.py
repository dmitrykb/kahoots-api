import web
from db.models import *
import http_errors

class AuthController():
    def __init__(self):
        self.user = None

    @classmethod
    def authorize(cls, f):        
        def wrapper(self, *args, **kwargs):
            print self
            if not self.find_user():
                return http_errors._401()
            return f(self, *args, **kwargs)
        return wrapper


    def find_user(self):
        # check if auth_token already exists in our database
        params = web.input()
        auth_token = web.ctx.orm.query(AuthToken).filter_by(token=params.auth_token).join(User).first()
        if auth_token and auth_token.user:
            self.user = auth_token.user
            return True
        return False