'''
Created on Jan 31, 2014

@author: korivka
'''
import json
from param import Param

class Validator():
    def __init__(self):
        self.is_valid = True
        self.params = []
        self.errors = []
    
    def parse_schema(self, schema):
        for field in schema:
            param = Param()
            param.name = field['name']
            param.type = field['type']
            if 'required' in field:
                param.required = field['required']
            if "allowed_values" in field:
                param.allowed_values = field['allowed_values']
            if "min_value" in field:
                param.min_value = field['min_value']
            if "max_value" in field:
                param.max_value = field['max_value']
            if "regex" in field:
                param.regex = field['regex']
            self.params.append(param)
            
    def validate(self, schema, post, get, headers):
        try:
            post = json.loads(post)
        except:
            pass

        self.parse_schema(schema)
        for param in self.params:
            if param.name in post:
                param.value = post[param.name]
            elif param.name in get:
                param.value = get[param.name]
            elif param.name in headers:
                param.value = headers[param.name]
            param.validate()
            if param.get_error_message():
                self.errors.append(param.get_error_message())
        return self.errors