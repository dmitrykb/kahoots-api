import web
import json

def bad_request(errors):
    headers = {"Content-Type": 'application/json'}
    data = {
        "errors": errors
    }
    raise web.HTTPError("404 Bad Request", data=json.dumps(data), headers=headers)