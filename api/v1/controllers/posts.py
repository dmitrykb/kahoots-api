import web
import json
import datetime
from api.v1.controllers.decorators import validate
from parser import Scraper
from db.models import *
from api.v1.controllers.auth_controller import AuthController
import http_errors
from sqlalchemy.sql import and_

class Posts(AuthController):

    post_schema = [{'name': 'HTTP_AUTHTOKEN', 'type': 'string', 'required':True},
                   {'name': 'url', 'type': 'string', 'required':True},
                   {'name': 'force_publish', 'type': 'enum','allowed_values': ['1','0'], 'required':False}]

    get_schema = [{'name': 'HTTP_AUTHTOKEN', 'type': 'string', 'required':True},
                   {'name': 'limit', 'type': 'int', 'required':False},
                   {'name': 'since', 'type': 'int', 'required':True},
                   # default gt: return posts that are later than 'since' param
                   {'name': 'direction', 'type': 'enum','allowed_values': ['gt','lt'], 'required':False}]

    '''
        POST /posts - create new post
    '''

    @validate(post_schema)
    @AuthController.authorize # sets self.user
    def POST(self):
        params = json.loads(web.data())
        try:
            scraper = Scraper(params['url'])
            scraper.parse()
        except:
            http_errors._400('Bad url.')

        post = Post()
        post.user_id = self.user.id
        post.title = scraper.data['title']
        post.description = scraper.data['description']
        post.image = scraper.data['image']
        post.host = scraper.data['host']
        post.type = scraper.data['type']
        post.site_name = scraper.data['site_name']
        post.site_icon = scraper.data['site_icon']
        post.url = scraper.data['url']
        post.charset = scraper.data['charset']        
        post.is_published = True if 'force_publish' not in params else params['force_publish']
        post.hash = post.generate_sum()

        # save new post
        web.ctx.orm.add(post)
        web.ctx.orm.commit()        

        return json.dumps(post.as_dict())



    '''
        GET /posts - get feed 
    '''

    @validate(get_schema)
    @AuthController.authorize # sets self.user
    def GET(self):
        params = web.input()
        limit = 0 if 'limit' not in params else int(params['limit'])

        try:
            since = str(datetime.datetime.fromtimestamp(float(params['since'])))
        except:
            http_errors._400('Wrong date format.')

        # OPTIMIZE THIS AND COVER WITH TESTS        
        if 'direction' not in params or params['direction'] == 'gt':
            posts = self.get_gt(since, limit)
        else:
            posts = self.get_lt(since, limit)
        ret = []
        for post in posts:            
            ret.append(post.as_dict())
        return json.dumps(ret[::-1]) # reversed


    def get_gt(self, since, limit):
        if limit > 0:
            posts = web.ctx.orm.query(Post)\
                .join(friends, Post.user_id == friends.c.friend_id)\
                .filter(\
                    and_(\
                        friends.c.user_id == self.user.id,\
                        Post.is_published == True,\
                        Post.created_timestamp > since\
                    )\
                )\
                .order_by(Post.created_timestamp.desc())\
                .limit(limit)
        else:
            posts = web.ctx.orm.query(Post)\
                .join(friends, Post.user_id == friends.c.friend_id)\
                .filter(\
                    and_(\
                        friends.c.user_id == self.user.id,\
                        Post.is_published == True,\
                        Post.created_timestamp > since\
                    )\
                )\
                .order_by(Post.created_timestamp.desc())\
                .all()
        return posts

    def get_lt(self, since, limit):
        if limit > 0:
            posts = web.ctx.orm.query(Post)\
                .join(friends, Post.user_id == friends.c.friend_id)\
                .filter(\
                    and_(\
                        friends.c.user_id == self.user.id,\
                        Post.is_published == True,\
                        Post.created_timestamp < since\
                    )\
                )\
                .order_by(Post.created_timestamp.desc())\
                .limit(limit)
        else:
            posts = web.ctx.orm.query(Post)\
                .join(friends, Post.user_id == friends.c.friend_id)\
                .filter(\
                    and_(\
                        friends.c.user_id == self.user.id,\
                        Post.is_published == True,\
                        Post.created_timestamp < since\
                    )\
                )\
                .order_by(Post.created_timestamp.desc())\
                .all()                
        return posts