from http import client
import pprint
from pydantic import BaseModel
from openai import OpenAI
from models.get_data import get_chat_statistics, get_chatbot, get_chatroom, get_userinfo, update_chatbot, update_chatroom
from models.talk_history import ChatRoom
from repository.database import add_all, db_session
from utils.utils import create_kakao_response
from models import dto


# 대화 내역을 저장할 리스트입니다.
talk_history = []

def get_gpt_response(client: OpenAI, message):
    response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": message}
                      ],
            max_tokens = 150,
            temperature = 0.7
            
        )

        # OpenAI로부터 받은 응답 메시지를 추출합니다.
    gpt_message = response.choices[0].message.content
    gpt_all = response
    print(gpt_message)
    return gpt_all


def service_test():
    chatroom_add()
    pass



## 채팅방 추가하기 & 채팅방 업데이트하기
def chatroom_add(chatroom : dto.Chatroom_add_datatype, db):
    
    json_data = {
        'user_id': chatroom['user_id'],
        'ai_id': chatroom['ai_id'],
        'chatbot_id': chatroom['chatbot_id'],
        
        # # 여기에 추가 정보를 포함시킵니다.
        # 'additional_info': {
        #     'user_context': {
        #         'username': chatroom['username'],
        #         'preferences': chatroom['preferences']
        #     },
        #     'session_details': {
        #         'location': chatroom['location'],
        #         'device': chatroom['device']
        #     }
        # }
    } 
    
    chatroom = add_all(json_data, 'ChatRoom', db)
    return chatroom

def chatroom_update(chatroom : dto.Chatbot_update_datatype, db):
    
    json_data = {
        'id': chatroom['id'],
        'user_id': chatroom['user_id'],
        'ai_id': chatroom['ai_id'],
        'chatbot_id': chatroom['chatbot_id'],
        
        # 여기에 추가 정보를 포함시킵니다.
        # 'additional_info': {
        #     'user_context': {
        #         'username': chatroom['username'],
        #         'preferences': chatroom['preferences']
        #     },
        #     'session_details': {
        #         'location': chatroom['location'],
        #         'device': chatroom['device']
        #     }
        # }
    } 
    
    chatroom = add_all(json_data, 'Chatroom', db)
    return chatroom


#지훈님
    ## AI 봇 추가하기 & AI 봇 업데이트하기 - 테이블 -> AI

def ai_add(AI : dto.AI_add_datatype, db):
    # AI 봇 추가 또는 업데이트 테스트
    json_data = {
        'name': AI['name'],
        'initial_prompt': AI['initial_prompt'],
        'max_tokens': AI['max_tokens'],
        'prompt_tokens': AI['prompt_tokens'],
        'completion_tokens': AI['completion_tokens'],
        'total_tokens': AI['total_tokens'],
        'ai_speech_log': AI['ai_speech_log']
    }

    ai = add_all(json_data, 'AI', db)
    return ai

def ai_update(AI : dto.AI_update_datatype, db):
    # AI 봇 추가 또는 업데이트 테스트
    json_data = {
        'id': AI['id'],
        'name': AI['name'],
        'initial_prompt': AI['initial_prompt'],
        'max_tokens': AI['max_tokens'],
        'prompt_tokens': AI['prompt_tokens'],
        'completion_tokens': AI['completion_tokens'],
        'total_tokens': AI['total_tokens'],
        'ai_speech_log': AI['ai_speech_log']
    }


    AI = add_all(json_data, 'AI', db)
    return AI

    ## 사용자 정보 추가하기 & 사용자 정보 업데이트하기 - 유저테이블
def user_add(User : dto.User_add_datatype, db):

    json_data = {
        'contact_info': User['contact_info'],
        'friend_status': User['friend_status'],
        'user_speech_log': User['user_speech_log']
    }

    User = add_all(json_data, 'User', db)
    return User

def user_update(User : dto.User_update_datatype, db):
    json_data = {
        'id': User['id'],
        'contact_info': User['contact_info'],
        'friend_status': User['friend_status'],
        'user_speech_log': User['user_speech_log']
    }


    User = add_all(json_data, 'User', db)
    print(User)
    return User


def userinfo_add(userinfo : dto.UserInfo_add_datatype, db):
    json_data = {
        'user_id': userinfo["user_id"],
        'image': userinfo["image"]
    }
    userinfo2 = add_all(json_data, 'UserInfo', db)
    return userinfo2

def userinfo_update(userinfo : dto.UserInfo_update_datatype, db):

    json_data = {
        'id': userinfo["id"],
        'user_id': userinfo["user_id"],
        # 'image': userinfo["image"]
    }
    userinfo = add_all(json_data, 'UserInfo', db)
    return userinfo

## GPT 정보 추가하기 & GPT 정보 업데이트하기 -> 챗봇테이블
def chatbot_add(chatbot : dto.Chatbot_add_datatype, db):

    json_data = {
        'name': chatbot["name"],
        'ai_id': chatbot["ai_id"]
    }
    chatbot = add_all(json_data, 'Chatbot', db)
    return chatbot

def chatbot_update(chatbot : dto.Chatbot_update_datatype, db):

    json_data = {
        'id': chatbot["id"],
        # 'name': chatbot["name"],
        'ai_id': chatbot["ai_id"]
    }
    chatbot = add_all(json_data, 'Chatbot', db)

    return chatbot


#나
##-ChatStatistics
## 챗봇 대화 정보 저장하기 & 챗봇 대화 정보 업데이트하기 -
## 엔드타임 생성 & 엔드타임 생성에 필요한 정보 주는 함수 - 테스트코드 없음
## 엔드타임 업데이트 - 테스트코드 참고

def ChatStatistics_add(ChatStatistics, db):
    json_data = {
        'chatroom_id' : ChatStatistics["chatroom_id"]
    }
    ChatStatistics = add_all(json_data, 'ChatStatistics', db)

    return new_chatStatistics

def ChatStatistics_update(ChatStatistics, db):
    json_data = {
        "id" : ChatStatistics["id"],
        'chatroom_id' : ChatStatistics["chatroom_id"]
    }
    ChatStatistics = add_all(json_data, 'ChatStatistics', db)

    return ChatStatistics

def ruser(User, AI, chatbot_name, db):
        
    new_user = user_add(User, db)
    new_userinfo = userinfo_add(create_userinfo(get_userinfo({"user_id": new_user.id,"image":"" }), new_user), db)
    new_ai = ai_add(AI, db)
    new_chatbot = chatbot_add(get_chatbot(chatbot_name, new_ai.id), db)
    new_chatroom = chatroom_add(get_chatroom(new_user.id, new_ai.id, new_chatbot.id), db)
    new_chatstatics = ChatStatistics_add(get_chat_statistics(new_chatroom.id), db)
    return ChatRoom(new_chatroom.id, new_ai.id, new_chatroom.chatbot_id, new_user.id, new_userinfo.id)

def create_userinfo(Userinfo:dto.UserInfo_add_datatype, new_user:dto.User_update_datatype):
    new_userinfo = {
        'user_id': new_user.id,
        'image': Userinfo['image'],
    }   
    return new_userinfo


def ruser_update(User, AI,  db, room : ChatRoom):

    new_user = user_update(User, db)
    new_userinfo = userinfo_update({"id" : room.get_userinfo_id(), "user_id": room.get_user_id()}, db)
    new_ai = ai_add(AI, db)
    new_chatbot = chatbot_update(update_chatbot(room.get_chatbot_id(), new_ai.id), db)
    new_chatroom = chatroom_update(update_chatroom(room.get_chatroom_id(), new_user.id, new_ai.id, new_chatbot.id), db)
    # new_chatstatics = ChatStatistics_add(get_chat_statistics(new_chatroom.id), db)
    # return ChatRoom(new_chatroom.id, new_ai.id, new_chatroom.chatbot_id, new_user.id)

    # user_update(User, db)
    # userinfo_update(Userinfo, db)
    # ai_update(AI, db)
    # chatbot_update(chatbot, db)
    # chatroom_update(chatroom, db)
    # ChatStatistics_update(chatStatitics, db)


def get_all_chat_room(db):
    chat_rooms = get_all_chat_rooms(db)
    return chat_rooms