from base_oauth_provider import BaseOAuthProvider
from facebook import GraphAPI, GraphAPIError
from oauth_user import OAuthUser
import http_errors


class FacebookOAuthProvider(BaseOAuthProvider):

    def __init__(self, auth_token):
        self.auth_token = auth_token
    
    def login(self):
        graph = GraphAPI(self.auth_token)
        try:
            profile = graph.get_object('me')
            picture = graph.get_object('me/picture?redirect=false&width=9999')
            print `picture`
        except GraphAPIError as error:
            errors = []
            errors.append(str(error))
            http_errors._400(errors)
            raise
        oauth_user = OAuthUser()
        oauth_user.email = profile['email']
        oauth_user.first_name = profile['first_name']
        oauth_user.last_name = profile['last_name']
        oauth_user.gender = profile['gender']
        oauth_user.timezone = profile['timezone']
        oauth_user.remote_id = profile['id']
        oauth_user.remote_avatar_url = picture['data']['url']
        oauth_user.is_silhouette = picture['data']['is_silhouette']
        return oauth_user
