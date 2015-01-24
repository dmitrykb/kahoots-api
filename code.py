import sys, os
abspath = os.path.dirname(__file__)
sys.path.append(abspath)
os.chdir(abspath)
import web
import json

from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine

engine = create_engine('mysql+mysqlconnector://root:qwerty@localhost/gc', echo=False)

def load_sqla(handler):
    web.ctx.orm = scoped_session(sessionmaker(bind=engine))
    web.header('Content-Type', 'application/json')
    try:
        return handler()
    except web.HTTPError:
        print 'httperror'
        web.ctx.orm.rollback()
        raise
    except:
        print 'error'
        web.ctx.orm.rollback()
        raise
    finally:
        web.ctx.orm.commit()

urls = (
        '/api/v1/users', 'api.v1.controllers.users.Users',
        '/api/v1/users/([0-9]+)/followers', 'api.v1.controllers.followers.Followers',
        '/api/v1/users/([0-9]+)/following', 'api.v1.controllers.following.Following',
        '/api/v1/following/([0-9]+)', 'api.v1.controllers.following.Following',
        '/api/v1/users/([0-9]+)/posts', 'api.v1.controllers.user_posts.UserPosts',
        '/api/v1/users/([\S\s]+)', 'api.v1.controllers.users.Users',
        '/api/v1/posts', 'api.v1.controllers.posts.Posts',
        '/api/v1/posts/([0-9]+)', 'api.v1.controllers.post.Post'
        )



app = web.application(urls, globals(), autoreload=True)
app.add_processor(load_sqla)
# app.notfound = notfound
# app.internalerror = internalerror

application = app.wsgifunc()
