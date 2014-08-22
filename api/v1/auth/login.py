import web

from validation.decorator import Validate

class Login:

    schema = [
        {'name':'email', 'type':'string', 'required':True}, 
        {'name': 'password', 'type': 'string', 'required':True} ]

    @Validate(schema)
    def POST(self):
        return 'post'

    @Validate(schema)
    def GET(self):
        return 'get'
