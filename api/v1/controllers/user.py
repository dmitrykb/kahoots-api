import web
import json
from api.v1.controllers.decorators import validate
from db.models import *
from api.v1.controllers.auth_controller import AuthController
import http_errors

class User(AuthController):
    put_schema = [{'name': 'HTTP_AUTHTOKEN', 'type': 'string', 'required':True},
              {'name': 'username', 'type': 'string', 'required':False},
              {'name': 'avatar_url', 'type': 'string', 'required':False}]

    @validate(put_schema)
    @AuthController.authorize # sets self.user
    def PUT(self, userid):
        # parse parameters
        params = json.loads(web.data())

        if int(self.user.id) != int(userid):
             raise http_errors._403()
        self.user.username = params.get('username', self.user.username)
        web.ctx.orm.add(self.user)
        web.ctx.orm.commit()
        return json.dumps(self.user.as_dict())

