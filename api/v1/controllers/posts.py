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

    post_schema = [{'name': 'auth_token', 'type': 'string', 'required':True},
                   {'name': 'url', 'type': 'string', 'required':True},
                   {'name': 'force_publish', 'type': 'enum','allowed_values': ['1','0'], 'required':False}]

    get_schema = [{'name': 'auth_token', 'type': 'string', 'required':True},
                   {'name': 'limit', 'type': 'int', 'required':False},
                   {'name': 'since', 'type': 'int', 'required':True}]

    '''
        POST /posts - create new post
    '''

    @validate(post_schema)
    @AuthController.authorize # sets self.user
    def POST(self):
        params = web.input()
        try:
            scraper = Scraper(params.url)
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
        post.is_published = False if 'force_publish' not in params else params.force_publish
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
        limit = 10 if 'limit' not in params else params.limit
        try:
            since = str(datetime.datetime.fromtimestamp(float(params.since)))
        except:
            http_errors._400('Wrong date format.')

        posts = web.ctx.orm.query(Post)\
            .join(friends, Post.user_id == friends.c.friend_id)\
            .filter(and_(
                Post.is_published == True,\
                Post.created_timestamp > since,\
                friends.c.user_id == self.user.id\
                ))\
            .limit(limit)
        
        ret = {u'posts':[]}
        for post in posts:            
            ret[u'posts'].append(post.as_dict())

        return json.dumps(ret)