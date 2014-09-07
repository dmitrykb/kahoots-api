import web
import json
from api.v1.controllers.decorators import validate
from parser import Scraper
from db.models import *
import urllib2, httplib
from api.v1.controllers.auth_controller import AuthController
import http_errors

class Posts(AuthController):

    post_schema = [{'name': 'auth_token', 'type': 'string', 'required':True},
                   {'name': 'url', 'type': 'string', 'required':True},
                   {'name': 'force_publish', 'type': 'enum','allowed_values': ['1','0'], 'required':False}]
    @validate(post_schema)
    @AuthController.authorize # sets self.user
    def POST(self):
        '''
            create new post
        '''
        params = web.input()
        try:
            scraper = Scraper(params.url)
            scraper.parse()
        except:
            http_errors.bad_request('Bad url.')

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
