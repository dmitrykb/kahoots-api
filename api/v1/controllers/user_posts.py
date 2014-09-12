import web
import json
import datetime
from api.v1.controllers.decorators import validate
from db.models import *
import urllib2, httplib
from api.v1.controllers.auth_controller import AuthController
import http_errors
from sqlalchemy.sql import and_


class UserPosts(AuthController):

    '''
        GET /users/{user_id}/posts - get posts made by specific user 
    '''

    get_schema = [{'name': 'auth_token', 'type': 'string', 'required':True},
                  {'name': 'since', 'type': 'int', 'required':False}]
    @validate(get_schema)
    @AuthController.authorize # sets self.user
    def GET(self, user_id):
        user = web.ctx.orm.query(User).filter_by(id=user_id).first()
        # 404
        if not user:
            return http_errors._404()
        params = web.input()

        try:
            since = str(datetime.datetime.fromtimestamp(float(params.since))) \
                    if u'since' in params\
                    else 0
        except:
            http_errors._400('Wrong date format.')        

        posts = web.ctx.orm.query(Post)\
            .filter(and_(
                Post.user_id == user_id,\
                Post.created_timestamp > since\
                ))
        
        ret = {u'posts':[]}
        for post in posts:            
            post_dict = post.as_dict()
            ret[u'posts'].append(post_dict)

        return json.dumps(ret)