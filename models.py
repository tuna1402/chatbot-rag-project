from sqlalchemy import Column, Integer, VARCHAR, Boolean, Text, DateTime, Interval, ForeignKey
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from base import engine, Base

Base = declarative_base()

# https://iwillcomplete.tistory.com/77 varchar와 text의 차이
# 

# AI
class AI(Base):
    __tablename__ = 'ai'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(VARCHAR(255))
    initial_prompt = Column(Text)
    max_tokens = Column(Integer)
    usage = Column(Text)
    ai_speech_log = Column(Text, default='[]')

# User
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    contact_info = Column(VARCHAR(255))
    friend_status = Column(Boolean)
    revisit_count = Column(Integer)
    user_speech_log = Column(Text, default='[]')

# Chatbot
class Chatbot(Base):
    __tablename__ = 'chatbot'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(VARCHAR(255))
    ai_id = Column(Integer, ForeignKey('ai.id'))

    ai = relationship('AI')

# ChatRoom
class ChatRoom(Base):
    __tablename__ = 'chatroom'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    ai_id = Column(Integer, ForeignKey('ai.id'))
    chatbot_id = Column(Integer, ForeignKey('chatbot.id'))
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    conversation_duration = Column(Interval)

    user = relationship('User')
    ai = relationship('AI')
    chatbot = relationship('Chatbot')

# UserInfo
class UserInfo(Base):
    __tablename__ = 'user_info'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    image = Column(VARCHAR(255))
    trend_design = Column(Text, default='[]')
    budget = Column(Integer)
    age = Column(Integer)
    region = Column(VARCHAR(255))

    user = relationship('User')

# ChatStatistics
class ChatStatistics(Base):
    __tablename__ = 'chat_statistics'

    id = Column(Integer, primary_key=True, autoincrement=True)
    chatroom_id = Column(Integer, ForeignKey('chatroom.id'))
    total_chat_duration = Column(Interval)
    average_chat_duration = Column(Interval)
    total_tokens = Column(Integer)
    average_tokens = Column(Integer)

    chatroom = relationship('ChatRoom')


Base.metadata.create_all(engine)
