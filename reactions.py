from sqlalchemy import Column, String, Integer, DateTime, func

from base import Base
class Reactions(Base):
    __tablename__ = 'reactions'
    id=Column(Integer, primary_key=True)
    message_id=Column(String(32))
    value=Column('value', String(32))
    user=Column('user', String(32))
    created=Column('created', DateTime, server_default=func.now())

def __init__(self, message_id, value, user):
        self.message_id = message_id
        self.value = value
        self.user = user