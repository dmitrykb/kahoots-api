import web
import json

def bad_request(errors):
    data = {
        "errors": errors
    }
    raise web.HTTPError("404 Bad Request", data=json.dumps(data))

def unauthorized():    
    data = {
        "errors": '401 Unauthorized. User not found.'
    }
    raise web.HTTPError("401 Unauthorized", data=json.dumps(data))