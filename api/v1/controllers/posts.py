import web
import json
import hashlib
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
    @AuthController.authorize
    def POST(self):
        params = web.input()
        # try:
        scraper = Scraper(params.url)
        scraper.parse()
        scraped_post = scraper.as_dict()
        # except:
        #     http_errors.bad_request('Bad url.')

        post = Post()
        post.user_id = self.user.id
        post.title = scraped_post['title']
        post.description = scraped_post['description']
        post.image = scraped_post['image']
        post.host = scraped_post['host']
        post.type = scraped_post['type']
        post.site_name = scraped_post['site_name']
        post.site_icon = scraped_post['site_icon']
        post.url = scraped_post['url']
        post.hash = self.checksum(post)

        post.is_published = False if 'force_publish' not in params else params.force_publish
        web.ctx.orm.add(post)
        web.ctx.orm.commit()        
        return json.dumps(post.as_dict())

    

    def checksum(self, post):
        m = hashlib.md5()
        m.update(post.title + post.host)
        return m.hexdigest()


    
