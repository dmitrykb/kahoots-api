from facebook_oauth_provider import FacebookOAuthProvider

class OAuthProviderFactory():

    @staticmethod
    def create_provider(oauth_provider, auth_token):
        if oauth_provider == 'FACEBOOK':
            return FacebookOAuthProvider(auth_token)
        elif oauth_provider == 'GOOGLE':
            return ""
        elif oauth_provider == 'KAHOOTS':
            return ""

        raise TypeError('Unknown Provider : \'' + oauth_provider + '\'. Allowed providers: ' + str(OAuthProviderFactory.providers))
