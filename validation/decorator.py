import web
from validator import Validator

class Validate(object):
    def __init__(self, schema):
        self.schema = schema
    def __call__(self, original_func):
        decorator_self = self
        def wrappee( *args, **kwargs):

            errors = Validator().validate(decorator_self.schema, web.input())
            if len(errors) == 0:
                # execute original http method
                return original_func(*args,**kwargs)
            web.ctx.status = '400 Bad Request'                
            return errors
        return wrappee
