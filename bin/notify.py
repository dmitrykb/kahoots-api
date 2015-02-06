'''
    Send push notifications
'''

import redis

if __name__ == "__main__":
    redis_cnx = redis.StrictRedis(host='localhost', port=6379, db=0)
    redis_cnx.rpush('users', 'asdf')
    redis_cnx.rpush('users', 'asdf1')
    redis_cnx.rpush('users', 'asdf2')
    redis_cnx.rpush('users1', 'users')
    users = redis_cnx.lrange('users1', 0, -1)
    print users


    user = {
            'id': '123',
            'ios_alert': 'You have something new to read.',
            'ios_payload': 'You have something new to read.',
            'android_payload': 'You have something new to read.',
            'android_collapse_key': '0',
            'client_type': 'ios',
            'push_token': '245o234u5o3ihjteiorti8934tu3450tu3490t45kl',
         }
