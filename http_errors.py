import web
import json

def _400(errors):
    data = {
        "errors": errors
    }
    print 'error 400'
    raise web.HTTPError("400 Bad Request", data=json.dumps(data))

def _401():
    data = {
        "errors": '401 Unauthorized'
    }
    raise web.HTTPError("401 Unauthorized", data=json.dumps(data))


def _404():
    data = {
        "errors": '404 Resource not found'
    }
    raise web.HTTPError("404 Not Found", data=json.dumps(data))


def _403():
    data = {
        "errors": '403 Write access forbidden'
    }
    return web.HTTPError("404 Write access forbidden", data=json.dumps(data))
