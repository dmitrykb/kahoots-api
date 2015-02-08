'''
    Get friends to notify
'''
import redis
import mysql.connector
from rq.decorators import job
import web
from db.models import *
from worker import conn
import config

from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine

from gcm import GCM


@job('default', connection=conn)
def startpush(user):
    engine = create_engine(config.db_url, echo=False)
    session = scoped_session(sessionmaker(bind=engine))
    pushtokens = session.query(PushToken)
    ios_tokens = []
    android_tokens = []
    for pushtoken in pushtokens:
        if pushtoken.client_type == PushToken.client_types[0]: #IOS
            ios_tokens.append(token)
        elif pushtoken.client_type == PushToken.client_types[1]: #ANDROID
            android_tokens.append(pushtoken.token)

    return notify_android(android_tokens)



def notify_android(tokens):
    gcm = GCM(config.gcm_api_key)
    data = {'type': 'new_posts'}
    response = gcm.json_request(registration_ids=tokens, data = data)

    return response
