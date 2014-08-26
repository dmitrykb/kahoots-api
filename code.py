import sys, os
abspath = os.path.dirname(__file__)
sys.path.append(abspath)
os.chdir(abspath)
import web
import json

from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine

engine = create_engine('mysql+mysqlconnector://root:qwerty@localhost/gc', echo=True)

def load_sqla(handler):
    web.ctx.orm = scoped_session(sessionmaker(bind=engine))
    web.header('Content-Type', 'application/json')
    try:
        return handler()
    except web.HTTPError:
        web.ctx.orm.rollback()
        raise
    except:
        web.ctx.orm.rollback()
        raise
    finally:
        web.ctx.orm.commit()

urls = (
        '/api/v1/login', 'api.v1.controllers.login.Login')

app = web.application(urls, globals(), autoreload=True)
app.add_processor(load_sqla)
# app.notfound = notfound
# app.internalerror = internalerror

application = app.wsgifunc()
