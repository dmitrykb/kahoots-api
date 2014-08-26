from sqlalchemy import create_engine, func
from sqlalchemy.orm import relationship, backref
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects import mysql



Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable = False)
    email = Column(String(70))
    created_timestamp = Column(DateTime(timezone=True), nullable = False, default=func.current_timestamp())
    last_seen_timestamp = Column(DateTime(timezone=True), nullable = False, default=func.current_timestamp(), onupdate=func.current_timestamp())
    is_removed = Column(Boolean, nullable = False, default = False, onupdate=func.current_timestamp())
    first_name = Column(String(50))
    last_name = Column(String(50))
    username = Column(String(50))

    def as_dict(self):
        user = {
                'id': self.id,
                'username': self.username, 
                'email': self.email,
                'created_timestamp': str(self.created_timestamp),
                'last_seen_timestamp': str(self.last_seen_timestamp),
                'is_removed': self.is_removed,
                'first_name': self.first_name,
                'last_name': self.last_name,
                'username': self.username}
        return user



class AuthToken(Base):
    __tablename__ = 'auth_tokens'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', backref='auth_tokens')
    token = Column(String(255))
    created_timestamp = Column(DateTime(timezone=True), nullable = False, default=func.current_timestamp())
    last_seen_timestamp = Column(DateTime(timezone=True), nullable = False, default=func.current_timestamp(), onupdate=func.current_timestamp())
    expires_in_sec = Column(Integer, nullable = False, default = 3200)
    oauth_provider = Column(mysql.ENUM('FACEBOOK', 'GOOGLE', 'GEECKCHAT'))

    def as_dict(self):
        ret = {
                'id': self.id,
                'user_id': self.user_id, 
                'token': self.token,
                'created_timestamp': str(self.created_timestamp),
                'last_seen_timestamp': str(self.last_seen_timestamp),
                'expires_in_sec': self.expires_in_sec,
                'oauth_provider': self.oauth_provider}
        return ret

