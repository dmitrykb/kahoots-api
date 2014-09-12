import web
import json
from api.v1.controllers.auth_controller import AuthController
from api.v1.controllers.decorators import validate
from db.models import *
import http_errors

class Following(AuthController):

    get_schema = [{'name': 'auth_token', 'type': 'string', 'required':True}]
    post_schema = [{'name': 'auth_token', 'type': 'string', 'required':True}]

    '''
        get list of friends (users, I follow)
    '''
    @validate(get_schema)
    @AuthController.authorize # sets self.user
    def GET(self, user_id):
        user = web.ctx.orm.query(User).filter_by(id=user_id).first()
        # 404
        if not user:
            return http_errors._404()

        friends = {u'users':[]}

        try:
            for user in user.following:
                friends[u'users'].append(user.as_dict())
            return json.dumps(friends)                
        except AttributeError:
            # 404
            return http_errors._404()



    '''
        follow new user
    '''
    @validate(post_schema)
    @AuthController.authorize # sets self.user
    def POST(self, user_id):

        # 400 if we're trying to friend ourselves
        if int(user_id) == int(self.user.id):
            return http_errors._400('You\'re trying to add yourself. Try to get some real friends.')


        new_friend = web.ctx.orm.query(User).filter_by(id=user_id).first()

        # 404 if user that we're trying to add was not found
        if not new_friend:
            return http_errors._404()

        self.user.following.append(new_friend)
        web.ctx.orm.commit()

        return ''



    '''
        unfollow new user
    '''
    @validate(post_schema)
    @AuthController.authorize # sets self.user
    def DELETE(self, user_id):

        old_friend = web.ctx.orm.query(User).filter_by(id=user_id).first()

        # 404 if user that we're trying to remove was not found
        if not old_friend:
            return http_errors._404()
        # 400 if user is not in the list of friends
        if old_friend not in self.user.following:
            return http_errors._400('You\'re not following this user')

        self.user.following.remove(old_friend)
        web.ctx.orm.commit()

        return ''
