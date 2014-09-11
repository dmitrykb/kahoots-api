import web
import json
from api.v1.controllers.auth_controller import AuthController
from api.v1.controllers.decorators import validate
from db.models import *
import http_errors

class Followers(AuthController):

    get_schema = [{'name': 'auth_token', 'type': 'string', 'required':True}]
    @validate(get_schema)
    @AuthController.authorize # sets self.user
    def GET(self, user_id):
        '''
            get list of users that subscribed to me
        '''

        user = web.ctx.orm.query(User).filter_by(id=user_id).first()
        followers = {u'users':[]}

        try:
            for user in user.followers:
                followers[u'users'].append(user.as_dict())
            return json.dumps(followers)                
        except AttributeError:
            #404
            return http_errors._400()
