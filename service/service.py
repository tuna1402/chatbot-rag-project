from http import client
import pprint
from pydantic import BaseModel
from openai import OpenAI
from repository.database import add_all, db_session, get_chat_rooms
from utils.utils import create_kakao_response
from models import dto


# 대화 내역을 저장할 리스트입니다.
talk_history = []

def get_gpt_response(client: OpenAI, message):
    print(f"get_gpt_responese", message)
    response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": message}
                      ],
            max_tokens = 150,
            temperature = 0.7
            
        )

        # OpenAI로부터 받은 응답 메시지를 추출합니다.
    gpt_message = response.choices[0].message.content
    print(gpt_message)
    return gpt_message


def service_test():
    chatroom_add()
    pass



## 채팅방 추가하기 & 채팅방 업데이트하기
def chatroom_add(chatroom : dto.Chatbot_add_datatype, db):
    
    json_data = {
        'user_id': chatroom['user_id'],
        'ai_id': chatroom['ai_id'],
        'chatbot_id': chatroom['chatbot_id'],
        
        # 여기에 추가 정보를 포함시킵니다.
        'additional_info': {
            'user_context': {
                'username': chatroom['username'],
                'preferences': chatroom['preferences']
            },
            'session_details': {
                'location': chatroom['location'],
                'device': chatroom['device']
            }
        }
    } 
    
    new_chatroom = add_all(json_data, 'ChatRoom', db)
    return new_chatroom

def chatroom_update(chatroom : dto.Chatbot_update_datatype, db):
    
    json_data = {
        'id': chatroom['id'],
        'user_id': chatroom['user_id'],
        'ai_id': chatroom['ai_id'],
        'chatbot_id': chatroom['chatbot_id'],
        
        # 여기에 추가 정보를 포함시킵니다.
        'additional_info': {
            'user_context': {
                'username': chatroom['username'],
                'preferences': chatroom['preferences']
            },
            'session_details': {
                'location': chatroom['location'],
                'device': chatroom['device']
            }
        }
    } 
    
    new_chatroom = add_all(json_data, 'Chatroom', db)
    return new_chatroom


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

    new_AI = add_all(json_data, 'AI', db)
    return new_AI

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


    new_AI = add_all(json_data, 'AI', db)
    return new_AI

    ## 사용자 정보 추가하기 & 사용자 정보 업데이트하기 - 유저테이블
def user_add(User : dto.User_add_datatype, db):

    print(f"user_add: ", User)
    json_data = {
        'contact_info': User['contact_info'],
        'friend_status': User['friend_status'],
        'user_speech_log': User['user_speech_log']
    }

    new_user = add_all(json_data, 'User', db)
    return new_user

def user_update(User : dto.User_update_datatype, db):
    json_data = {
        'id': User['id'],
        'contact_info': User['contact_info'],
        'friend_status': User['friend_status'],
        'user_speech_log': User['user_speech_log']
    }

    new_user = add_all(json_data, 'User', db)
    return new_user

#다인님
## 사용자 메시지 로그 저장하기 - 보수공사 후 진행 ->유저인포테이블
## GPT 정보 추가하기 & GPT 정보 업데이트하기 -> 챗봇테이블
#다인님
## 사용자 메시지 로그 저장하기 - 보수공사 후 진행 ->유저인포테이블
def userinfo_add(userinfo : dto.UserInfo_add_datatype, db):
    json_data = {
        'user_id': userinfo["user_id"],
        'image': userinfo["image"]
    }
    new_userinfo = add_all(json_data, 'UserInfo', db)
    return new_userinfo

def userinfo_update(userinfo : dto.UserInfo_update_datatype, db):

    json_data = {
        'id': userinfo["id"],
        'user_id': userinfo["user_id"],
        'image': userinfo["image"]
    }
    new_userinfo = add_all(json_data, 'UserInfo', db)
    return new_userinfo

## GPT 정보 추가하기 & GPT 정보 업데이트하기 -> 챗봇테이블
def chatbot_add(chatbot : dto.Chatbot_add_datatype, db):

    json_data = {
        'name': chatbot["name"],
        'ai_id': chatbot["ai_id"]
    }
    new_chatbot = add_all(json_data, 'Chatbot', db)
    
    return new_chatbot

def chatbot_update(chatbot : dto.Chatbot_update_datatype, db):

    json_data = {
        'id': chatbot["id"],
        'name': chatbot["name"],
        'ai_id': chatbot["ai_id"]
    }
    new_chatbot = add_all(json_data, 'Chatbot', db)

    return new_chatbot


#나
##-ChatStatistics
## 챗봇 대화 정보 저장하기 & 챗봇 대화 정보 업데이트하기 -
## 엔드타임 생성 & 엔드타임 생성에 필요한 정보 주는 함수 - 테스트코드 없음
## 엔드타임 업데이트 - 테스트코드 참고

def ChatStatistics_add(ChatStatistics, db):
    json_data = {
        'chatroom_id' : ChatStatistics["chatroom_id"]
    }
    new_chatStatistics = add_all(json_data, 'ChatStatistics', db)

    return new_chatStatistics

def ChatStatistics_update(ChatStatistics, db):
    json_data = {
        "id" : ChatStatistics["id"],
        'chatroom_id' : ChatStatistics["chatroom_id"]
    }
    new_chatStatistics = add_all(json_data, 'ChatStatistics', db)

    return new_chatStatistics

def ruser(User, Userinfo, AI, chatbot, chatroom, chatStatitics, db):
    print(f"ruser: ", User)
    user_add(User, db)
    userinfo_add(Userinfo, db)
    ai_add(AI, db)
    chatbot_add(chatbot, db)
    chatroom_add(chatroom, db)
    ChatStatistics_add(chatStatitics, db)
        


def ruser_update(User, Userinfo, AI, chatbot, chatroom, chatStatitics, db):
    user_update(User, db)
    userinfo_update(Userinfo, db)
    ai_update(AI, db)
    chatbot_update(chatbot, db)
    chatroom_update(chatroom, db)
    ChatStatistics_update(chatStatitics, db)


def get_chatrooms(db):
    chat_rooms = get_chat_rooms(db)
    return chat_rooms