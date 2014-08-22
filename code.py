import sys, os
abspath = os.path.dirname(__file__)
sys.path.append(abspath)
os.chdir(abspath)


import web
import json


def notfound():
    return json.dumps({'ok':0, 'errcode': 404})

def internalerror():
    return json.dumps({'ok':0, 'errcode': 500})



urls = (
        '/api/v1/login', 'api.v1.auth.login.Login')

app = web.application(urls, globals(), autoreload=True)
# app.notfound = notfound
# app.internalerror = internalerror

application = app.wsgifunc()

