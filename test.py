import pytest
import json
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from datetime import datetime, timedelta
from models import AI, User, Chatbot, ChatRoom, UserInfo, ChatStatistics
from database import (
    ai_add_or_update_data,
    user_add_or_update_data,
    chatbot_add_data,
    chatroom_add_or_update,
    userinfo_add_or_update_data,
    chat_statistics_add_or_update_data,
    update_end_time
)

DATABASE_URL = "postgresql://postgres:password@localhost/chatbot"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=True, bind=engine)

@pytest.fixture(scope="function")
def db_session():
    # 새로운 데이터베이스 세션을 생성합니다.
    connection = engine.connect()
    transaction = connection.begin()
    session = SessionLocal(bind=connection)
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()

# def test_ai_add_or_update(db_session):
#     json_data = {
#         'id': 1,
#         'name': 'Test AI',
#         'initial_prompt': 'Hello',
#         'max_tokens': 100,
#         'prompt_tokens': 40,
#         'completion_tokens': 30,
#         'total_tokens': 70,
#         'ai_speech_log': '["오늘 날씨 어떄?"]'
#     }
#     ai = ai_add_or_update_data(json_data)
#     assert ai.name == 'Test AI'
#     assert ai.max_tokens == 100
#     assert json.loads(ai.usage)['total_tokens'] == 70

# def test_user_add_or_update(db_session):
#     json_data = {
#         'id': 1,
#         'contact_info': 'test1@example.com',
#         'friend_status': True,
#         'user_speech_log': '["반가워요"]'
#     }
#     user = user_add_or_update_data(json_data)
#     assert user.contact_info == 'test1@example.com'
#     assert user.friend_status is True
#     assert json.loads(user.user_speech_log) == ['안녕하세요', '반가워요', '반가워요']

# def test_chatbot_add_data(db_session):
#     json_data = {
#         'id': 2,
#         'name': 'Test Chatbot',
#         'ai_id': 2
#     }
#     chatbot = chatbot_add_data(json_data)
#     assert chatbot.name == 'Test Chatbot'
#     assert chatbot.ai_id == 2

# def test_chatroom_add_or_update(db_session):
#     json_data = {
#         'id': 1,
#         'user_id': 1,
#         'ai_id': 1,
#         'chatbot_id': 1
#     }
#     chatroom = chatroom_add_or_update(json_data)
#     assert chatroom.user_id == 1
#     assert chatroom.ai_id == 1
#     assert chatroom.chatbot_id == 1

# def test_userinfo_add_or_update(db_session):
#     json_data = {
#         'id': 1,
#         'user_id': 1,
#         'image': 'image.png',
#         'trend_design': '["Design2"]',
#         'budget': 1000,
#         'age': 25,
#         'region': 'Region1'
#     }
#     userinfo = userinfo_add_or_update_data(json_data)
#     assert userinfo.image == 'image.png'
#     assert json.loads(userinfo.trend_design) == ['Design2']
#     assert userinfo.budget == 1000

# def test_chat_statistics_add_or_update(db_session):
#     json_data = {
#         'id': 1,
#         'chatroom_id': 1
#     }
#     chat_statistics = chat_statistics_add_or_update_data(json_data)
#     assert chat_statistics.chatroom_id == 1

# def test_update_end_time(db_session):
#     # 먼저 ChatRoom과 관련된 데이터를 추가합니다.
#     chatroom_data = {
#         'id': 1,
#         'user_id': 1,
#         'ai_id': 1,
#         'chatbot_id': 1
#     }
#     chatroom = chatroom_add_or_update(chatroom_data)
    
#     # end_time 업데이트를 테스트합니다.
#     update_data = {
#         'id': 1,
#         'end_time': datetime.utcnow().isoformat()
#     }
#     update_end_time(update_data)
    
#     chatroom_updated = db_session.query(ChatRoom).filter(ChatRoom.id == 1).first()
#     assert chatroom_updated.end_time is not None
#     assert chatroom_updated.conversation_duration is not None

if __name__ == "__main__":
    pytest.main()