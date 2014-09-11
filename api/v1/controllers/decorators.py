import web
import json

from validation.validator import Validator
import http_errors

class validate(object):
    '''
        @validate(schema)
        Decorator that is used in controller, before each http request
        Returns controller's method or 400 Bad Request
    '''
    def __init__(self, schema):
        self.schema = schema
    def __call__(self, original_func):
        decorator_self = self
        def wrappee( *args, **kwargs):

            errors = Validator().validate(decorator_self.schema, web.input())
            if len(errors) > 0:
                # raise 400
                http_errors._400(errors)

            # execute original http method
            return original_func(*args,**kwargs)
        return wrappee
