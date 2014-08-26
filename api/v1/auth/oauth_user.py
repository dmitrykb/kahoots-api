class OAuthUser():

    def __init__(self):
        self.email = None
        self.first_name = None
        self.last_name = None
        self.gender = None
        self.timezone = None
        self.remote_id = None
        self.remote_avatar_url = None


    def as_dict(self):
        user = {
                'email': self.email,
                'first_name': self.first_name, 
                'last_name': self.last_name,
                'gender': self.gender,
                'timezone': self.timezone,
                'remote_id': self.remote_id,
                'remote_avatar_url': self.remote_avatar_url}
        return user
