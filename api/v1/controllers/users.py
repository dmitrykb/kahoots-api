import web
import json

from api.v1.controllers.decorators import validate
from db.models import *
from api.v1.auth.oauth_provider_factory import OAuthProviderFactory
from sqlalchemy.sql import and_, or_

class Users():

    schema = [{'name': 'HTTP_AUTH_TOKEN', 'type': 'string', 'required':True},
              {'name': 'oauth_provider', 'type': 'enum', 'allowed_values': AuthToken.providers, 'required':True},
              {'name': 'expires_in_sec', 'type': 'string', 'required':True},
              {'name': 'push_token', 'type': 'string', 'required':True},
              {'name': 'client_type', 'type': 'enum', 'allowed_values': ['IOS','ANDROID'], 'required':True},
              {'name': 'client_version', 'type': 'string', 'required':True}]

    @validate(schema)
    def POST(self):
        # parse parameters
        params = json.loads(web.data())
        headers = web.ctx.env

        # check if auth_token already exists in our database
        auth_token = web.ctx.orm.query(AuthToken).filter_by(token=headers['HTTP_AUTH_TOKEN']).join(User).first()
        if auth_token and auth_token.user:            
            return json.dumps(auth_token.user.as_dict())

        # check if push_token and user exist
        push_token = web.ctx.orm.query(PushToken).filter_by(token=params['push_token']).join(User).first()
        if push_token and push_token.user:
            auth_token = AuthToken()
            auth_token.token = headers['HTTP_AUTH_TOKEN']
            auth_token.oauth_provider = params['oauth_provider']
            auth_token.expires_in_sec = params['expires_in_sec']
            auth_token.push_token_id = push_token.id
            push_token.user.auth_tokens.append(auth_token)
            web.ctx.orm.add(push_token.user)
            web.ctx.orm.commit()
            return json.dumps(push_token.user.as_dict())

        
        # create oauth provider, based on oauth provider
        oauth_provider = OAuthProviderFactory.create_provider(auth_token = headers['HTTP_AUTH_TOKEN'], oauth_provider = params['oauth_provider'])
        oauth_user = oauth_provider.login()

        # check if user with oauth_user.email is already regostered the database
        user = web.ctx.orm.query(User).filter_by(email=oauth_user.email).first()

        # save new auth_token
        auth_token = AuthToken()
        auth_token.token = headers['HTTP_AUTH_TOKEN']
        auth_token.oauth_provider = params['oauth_provider']
        auth_token.expires_in_sec = params['expires_in_sec']

        # save new push_token
        avatar = Avatar()
        avatar.remote_url = oauth_user.remote_avatar_url
        avatar.url = oauth_user.remote_avatar_url
        avatar.is_silhouette = oauth_user.is_silhouette

        # save new avatar
        push_token = PushToken()
        push_token.token = params['push_token']
        push_token.client_type = params['client_type']
        push_token.client_version = params['client_version']
        push_token.auth_tokens.append(auth_token)

        if not user:
            # create new user in database
            user = User()
            user.email = oauth_user.email
            user.first_name = oauth_user.first_name
            user.last_name = oauth_user.last_name

        user.push_tokens.append(push_token)
        user.auth_tokens.append(auth_token)
        user.avatars.append(avatar)
        web.ctx.orm.add(user)
        web.ctx.orm.commit()

        return json.dumps(user.as_dict())


    get_schema = [{'name': 'HTTP_AUTH_TOKEN', 'type': 'string', 'required':True}]
    @validate(get_schema)
    def GET(self, pattern):
        '''
            search users by @pattern [\W\w]+
        '''

        pattern = '%' + pattern + '%'
        users = web.ctx.orm.query(User)\
                    .filter(\
                        and_(
                            or_(User.email.like(pattern),\
                                User.username.like(pattern),\
                                User.first_name.like(pattern),\
                                User.last_name.like(pattern)\
                                ),\
                               User.is_removed == False 
                            )
                        ).limit(30)
        ret = {u'users':[]}
        for user in users:
            ret[u'users'].append(user.as_dict())

        return json.dumps(ret)


