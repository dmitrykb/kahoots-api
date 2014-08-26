import web
import json
from  sqlalchemy import create_engine

from api.v1.controllers.decorators import validate
from db.models import *
from api.v1.auth.oauth_provider_factory import OAuthProviderFactory

class Login():

    schema = [{'name': 'auth_token', 'type': 'string', 'required':True},
              {'name': 'oauth_provider', 'type': 'enum', 'allowed_values': OAuthProviderFactory.providers, 'required':True},
              {'name': 'expires_in_sec', 'type': 'string', 'required':True}]

    @validate(schema)
    def POST(self):

        # parse parameters
        params = web.input()
        auth_token_param = params.auth_token
        oauth_provider_param = params.oauth_provider
        expires_in_sec_param = params.expires_in_sec

        # check if user already exists in our database
        auth_token = web.ctx.orm.query(AuthToken).filter_by(token=auth_token_param).join(User).first()

        if auth_token and auth_token.user:
            return json.dumps(auth_token.user.as_dict())

        # create oauth provider, based on oauth provider
        oauth_provider = OAuthProviderFactory.create_provider(auth_token = auth_token_param, oauth_provider = oauth_provider_param)
        oauth_user = oauth_provider.login()


        # check if user with oauth_user.email is already in the database
        user = web.ctx.orm.query(User).filter_by(email=oauth_user.email).first()
        if not user:
            # create new user in database
            user = User()
            user.email = oauth_user.email
            user.first_name = oauth_user.first_name
            user.last_name = oauth_user.last_name

        # save new auth_token
        auth_token = AuthToken()
        auth_token.token = auth_token_param
        auth_token.oauth_provider = oauth_provider_param
        auth_token.expires_in_sec = expires_in_sec_param
        user.auth_tokens.append(auth_token)
        web.ctx.orm.add(user)
        web.ctx.orm.commit()

        return json.dumps(user.as_dict())

