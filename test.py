# from sqlalchemy.orm import Session
# from models import AI, User, Chatbot, ChatRoom, UserInfo, ChatStatistics
# from base import SessionLocal
# from database import add_all, ai_add_or_update_data, user_add_or_update_data, chatbot_add_data, chatroom_add_data, userinfo_add_or_update_data, chat_statistics_add_or_update_data, time_and_token_search

# # AI 테이블에 대한 테스트
# def test_ai_insert_and_update():
#     json_data = {
#         "id": 2,
#         "name": "Test AI",
#         "initial_prompt": "Hello",
#         "max_tokens": 100,
#         "prompt_tokens": 10,
#         "completion_tokens": 20,
#         "total_tokens": 50,
#         "ai_speech_log": '["안녕하세요!"]'
#     }

#     ai_add_or_update_data(json_data)

#     # # 데이터베이스에서 데이터 확인
#     # with SessionLocal() as db:
#     #     ai = db.query(AI).filter(AI.id == 1).first()
#     #     print(ai)

#     # # 업데이트 데이터
#     # update_data = {
#     #     "id": 1,
#     #     "name": "Updated AI",
#     #     "initial_prompt": "Hi",
#     #     "max_tokens": 200,
#     #     "prompt_tokens": 15,
#     #     "completion_tokens": 25,
#     #     "total_tokens": 40,
#     #     "ai_speech_log": '["AI 챗봇을 사용해보세요!"]'
#     # }

#     # ai_add_or_update_data(update_data)

#     # 데이터베이스에서 데이터 확인
#     with SessionLocal() as db:
#         ai = db.query(AI).filter(AI.id == 1).first()
#         print(ai)

# # User 테이블에 대한 테스트
# def test_user_insert_and_update():
#     json_data = {
#         "id": 1,
#         "contact_info": "test",
#         "friend_status": True,
#         "revisit_count": 5,
#         "user_speech_log": '["안녕하세요"]'
#     }

#     user_add_or_update_data(json_data)

#     # 데이터베이스에서 데이터 확인
#     with SessionLocal() as db:
#         user = db.query(User).filter(User.id == 1).first()
#         print(user)

#     # 업데이트 데이터
#     update_data = {
#         "id": 1,
#         "contact_info": "test@naver.com",
#         "friend_status": False,
#         "revisit_count": 10,
#         "user_speech_log": '["인테리어 정보는 어디다 물어봐야 할까?"]'
#     }

#     user_add_or_update_data(update_data)

#     # 데이터베이스에서 데이터 확인
#     with SessionLocal() as db:
#         user = db.query(User).filter(User.id == 1).first()
#         print(user)

# # Chatbot 테이블에 대한 테스트
# def test_chatbot_insert():
#     json_data = {
#         "id": 1,
#         "name": "Test Chatbot",
#         "ai_id": 1
#     }

#     chatbot = chatbot_add_data(json_data)

#     print("Chatbot Added:")
#     print(f"ID: {chatbot.id}")
#     print(f"Name: {chatbot.name}")
#     print(f"AI ID: {chatbot.ai_id}")

# # ChatRoom 테이블에 대한 테스트
# def test_chatroom_insert():
#     json_data = {
#         "id": 1,
#         "user_id": 1,
#         "ai_id": 1,
#         "chatbot_id": 1,
#         "start_time": "2024-08-27T10:00:00",
#         "end_time": "2024-08-27T10:30:00"
#     }

#     chatroom = chatroom_add_data(json_data)

#     print("ChatRoom Added:")
#     print(f"ID: {chatroom.id}")
#     print(f"User ID: {chatroom.user_id}")
#     print(f"AI ID: {chatroom.ai_id}")
#     print(f"Chatbot ID: {chatroom.chatbot_id}")
#     print(f"Start Time: {chatroom.start_time}")
#     print(f"End Time: {chatroom.end_time}")
#     print(f"Conversation Duration: {chatroom.conversation_duration}")

# # UserInfo 테이블에 대한 테스트
# def test_userinfo_insert_and_update():
#     json_data = {
#         "id": 1,
#         "user_id": 1,
#         "image": "profile.jpg",
#         "trend_design": '["modern", "minimalist"]',
#         "budget": 1000,
#         "age": 30,
#         "region": "서울"
#     }

#     userinfo_add_or_update_data(json_data)

#     # 데이터베이스에서 데이터 확인
#     with SessionLocal() as db:
#         userinfo = db.query(UserInfo).filter(UserInfo.id == 1).first()
#         print(userinfo)

#     # 업데이트 데이터
#     update_data = {
#         "id": 1,
#         "user_id": 1,
#         "image": "updated_profile.jpg",
#         "trend_design": '["classic"]',
#         "budget": 1000,
#         "age": 30,
#         "region": "서울"
#     }

#     userinfo_add_or_update_data(update_data)

#     # 데이터베이스에서 데이터 확인
#     with SessionLocal() as db:
#         userinfo = db.query(UserInfo).filter(UserInfo.id == 1).first()
#         print(userinfo)

# # ChatStatistics 테이블에 대한 테스트
# def test_chatstatistics_insert_and_update():
#     json_data = {
#         "id": 1,
#         "chatroom_id": 1,
#         "average_chat_duration": 1800,
#         "average_tokens": 75
#     }

#     chat_statistics_add_or_update_data(json_data)  # 데이터 삽입

#     # 데이터베이스에서 데이터 확인
#     with SessionLocal() as db:
#         statistics = db.query(ChatStatistics).filter(ChatStatistics.id == 1).first()
#         print(statistics)


# def test_time_and_token_search():
#     result = time_and_token_search(1)
    
#     if result:
#         print("Current Time:", result["current_time"])
#         print("End Time:", result["end_time"])
#         print("Total Tokens:", result["total_tokens"])
#     else:
#         print("ChatRoom not found.")

# # 테스트 실행
# test_ai_insert_and_update()
# test_user_insert_and_update()
# test_chatbot_insert()
# test_chatroom_insert()
# test_userinfo_insert_and_update()
# test_chatstatistics_insert_and_update()
# test_time_and_token_search()

# def test_user_insert_via_add_all():
#     json_data = {
#         "id": 1,
#         "contact_info": "test@naver.com",
#         "friend_status": True,
#         "revisit_count": 5,
#         "user_speech_log": '["안녕하세요?"]'
#     }

#     # add_all 함수를 이용하여 users 테이블에 데이터를 삽입합니다.
#     add_all(json_data, 'User')

#     with SessionLocal() as db:
#         user = db.query(User).filter(User.id == json_data['id']).first()
#         if user:
#             print(f"ID: {user.id}")
#             print(f"Contact Info: {user.contact_info}")
#             print(f"Friend Status: {user.friend_status}")
#             print(f"Revisit Count: {user.revisit_count}")
#             print(f"User Speech Log: {user.user_speech_log}")
#         else:
#             print("User 데이터가 존재하지 않습니다.")

# # 테스트 실행
# test_user_insert_via_add_all()











# from sqlalchemy.orm import Session
# from models import AI, User, Chatbot, ChatRoom, UserInfo, ChatStatistics
# from base import SessionLocal
# from database import add_all, ai_add_or_update_data, user_add_or_update_data, chatbot_add_data, chatroom_add_data, userinfo_add_or_update_data, chat_statistics_add_or_update_data, time_and_token_search

# # AI 테이블에 대한 테스트
# def test_ai_insert_and_update():
#     json_data = {
#         "id": 2,
#         "name": "Test AI",
#         "initial_prompt": "Hello",
#         "max_tokens": 100,
#         "prompt_tokens": 10,
#         "completion_tokens": 20,
#         "total_tokens": 30,
#         "ai_speech_log": '["반가워요!"]'
#     }

#     ai_add_or_update_data(json_data)

#     # 데이터베이스에서 데이터 확인
#     with SessionLocal() as db:
#         ai = db.query(AI).filter(AI.id == 1).first()
#         print(ai)

#     # # 업데이트 데이터
#     # update_data = {
#     #     "id": 1,
#     #     "name": "Updated AI",
#     #     "initial_prompt": "Hi",
#     #     "max_tokens": 200,
#     #     "prompt_tokens": 15,
#     #     "completion_tokens": 25,
#     #     "total_tokens": 40,
#     #     "ai_speech_log": '["AI 챗봇을 사용해보세요!"]'
#     # }

#     # ai_add_or_update_data(update_data)

#     # 데이터베이스에서 데이터 확인
#     with SessionLocal() as db:
#         ai = db.query(AI).filter(AI.id == 1).first()
#         print(ai)

# # User 테이블에 대한 테스트
# def test_user_insert_and_update():
#     json_data = {
#         "id": 2,
#         "contact_info": "test",
#         "friend_status": True,
#         "revisit_count": 5,
#         "user_speech_log": '["안녕하세요"]'
#     }

#     user_add_or_update_data(json_data)

#     # 데이터베이스에서 데이터 확인
#     with SessionLocal() as db:
#         user = db.query(User).filter(User.id == 1).first()
#         print(user)

#     # 업데이트 데이터
#     update_data = {
#         "id": 2,
#         "contact_info": "test@naver.com",
#         "friend_status": False,
#         "revisit_count": 10,
#         "user_speech_log": '["인테리어 정보는 어디다 물어봐야 할까?"]'
#     }

#     user_add_or_update_data(update_data)

#     # 데이터베이스에서 데이터 확인
#     with SessionLocal() as db:
#         user = db.query(User).filter(User.id == 1).first()
#         print(user)

# # Chatbot 테이블에 대한 테스트
# def test_chatbot_insert():
#     json_data = {
#         "id": 2,
#         "name": "Test Chatbot",
#         "ai_id": 2
#     }

#     chatbot = chatbot_add_data(json_data)

#     print("Chatbot Added:")
#     print(f"ID: {chatbot.id}")
#     print(f"Name: {chatbot.name}")
#     print(f"AI ID: {chatbot.ai_id}")

# # ChatRoom 테이블에 대한 테스트
# def test_chatroom_insert():
#     json_data = {
#         "id": 2,
#         "user_id": 2,
#         "ai_id": 2,
#         "chatbot_id": 2,
#         "start_time": "2024-08-27T10:00:00",
#         "end_time": "2024-08-27T10:30:00"
#     }

#     chatroom = chatroom_add_data(json_data)

#     print("ChatRoom Added:")
#     print(f"ID: {chatroom.id}")
#     print(f"User ID: {chatroom.user_id}")
#     print(f"AI ID: {chatroom.ai_id}")
#     print(f"Chatbot ID: {chatroom.chatbot_id}")
#     print(f"Start Time: {chatroom.start_time}")
#     print(f"End Time: {chatroom.end_time}")
#     print(f"Conversation Duration: {chatroom.conversation_duration}")

# # UserInfo 테이블에 대한 테스트
# def test_userinfo_insert_and_update():
#     json_data = {
#         "id": 2,
#         "user_id": 2,
#         "image": "profile.jpg",
#         "trend_design": '["modern", "minimalist"]',
#         "budget": 1000,
#         "age": 30,
#         "region": "서울"
#     }

#     userinfo_add_or_update_data(json_data)

#     # 데이터베이스에서 데이터 확인
#     with SessionLocal() as db:
#         userinfo = db.query(UserInfo).filter(UserInfo.id == 1).first()
#         print(userinfo)

#     # 업데이트 데이터
#     update_data = {
#         "id": 2,
#         "user_id": 2,
#         "image": "updated_profile.jpg",
#         "trend_design": '["classic"]',
#         "budget": 1000,
#         "age": 30,
#         "region": "서울"
#     }

#     userinfo_add_or_update_data(update_data)

#     # 데이터베이스에서 데이터 확인
#     with SessionLocal() as db:
#         userinfo = db.query(UserInfo).filter(UserInfo.id == 1).first()
#         print(userinfo)

# # ChatStatistics 테이블에 대한 테스트
# def test_chatstatistics_insert_and_update():
#     json_data = {
#         "id": 2,
#         "chatroom_id": 2,
#         "average_chat_duration": 1800,
#         "average_tokens": 75
#     }

#     chat_statistics_add_or_update_data(json_data)  # 데이터 삽입

#     # 데이터베이스에서 데이터 확인
#     with SessionLocal() as db:
#         statistics = db.query(ChatStatistics).filter(ChatStatistics.id == 1).first()
#         print(statistics)


# def test_time_and_token_search():
#     result = time_and_token_search(1)
    
#     if result:
#         print("Current Time:", result["current_time"])
#         print("End Time:", result["end_time"])
#         print("Total Tokens:", result["total_tokens"])
#     else:
#         print("ChatRoom not found.")

# # 테스트 실행
test_ai_insert_and_update()
# test_user_insert_and_update()
# test_chatbot_insert()
# test_chatroom_insert()
# test_userinfo_insert_and_update()
# test_chatstatistics_insert_and_update()
# test_time_and_token_search()

# def test_user_insert_via_add_all():
#     json_data = {
#         "id": 2,
#         "contact_info": "test@naver.com",
#         "friend_status": True,
#         "revisit_count": 5,
#         "user_speech_log": '["안녕하세요?"]'
#     }

#     # add_all 함수를 이용하여 users 테이블에 데이터를 삽입합니다.
#     add_all(json_data, 'User')

#     with SessionLocal() as db:
#         user = db.query(User).filter(User.id == json_data['id']).first()
#         if user:
#             print(f"ID: {user.id}")
#             print(f"Contact Info: {user.contact_info}")
#             print(f"Friend Status: {user.friend_status}")
#             print(f"Revisit Count: {user.revisit_count}")
#             print(f"User Speech Log: {user.user_speech_log}")
#         else:
#             print("User 데이터가 존재하지 않습니다.")

# # 테스트 실행
# test_user_insert_via_add_all()