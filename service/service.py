from http import client
import pprint

from openai import OpenAI
from repository.database import add_all, db_session
from utils.utils import create_kakao_response


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
def chatroom_add(chatroom):
    
    json_data = {
        'id': chatroom.id,
        'user_id': chatroom.user_id,
        'ai_id': chatroom.ai_id,
        'chatbot_id': chatroom.chatbot_id,
        
        # 여기에 추가 정보를 포함시킵니다.
        'additional_info': {
            'user_context': {
                'username': chatroom.username,
                'preferences': chatroom.preferences
            },
            'session_details': {
                'location': chatroom.location,
                'device': chatroom.device
            }
        }
    }        
    # # 메모리에서의 값을 print로 출력합니다.
    # print(f"id: {id}")
    # print(f"user_id: {user_id}")
    # print(f"ai_id: {ai_id}")
    # print(f"chatbot_id: {chatbot_id}")
    # print(f"Username: {username}")
    # print(f"Preferences: {preferences}")
    # print(f"Location: {location}")
    # print(f"Device: {device}")
    
    
    chatroom = add_all(json_data, 'Chatroom')
    return chatroom


#지훈님
    ## AI 봇 추가하기 & AI 봇 업데이트하기 - 테이블 -> AI

def ai_add(AI):
    # AI 봇 추가 또는 업데이트 테스트
    json_data = {
        'id': AI.id,
        'name': AI.name,
        'initial_prompt': AI.initial_prompt,
        'max_tokens': AI.max_tokens,
        'prompt_tokens': AI.prompt_tokens,
        'completion_tokens': AI.completion_tokens,
        'total_tokens': AI.total_tokens,
        'ai_speech_log': AI.ai_speech_log
    }


    AI = add_all(json_data, 'AI')
    return AI

    ## 사용자 정보 추가하기 & 사용자 정보 업데이트하기 - 유저테이블
def user_add(User,db):
    json_data = {
        'id': User.id,
        'contact_info': User.contact_info,
        'friend_status': User.friend_status,
        'user_speech_log': User.user_speech_log
    }

    User = add_all(json_data, 'User', db)
    return User


#다인님
## 사용자 메시지 로그 저장하기 - 보수공사 후 진행 ->유저인포테이블
## GPT 정보 추가하기 & GPT 정보 업데이트하기 -> 챗봇테이블
#다인님
## 사용자 메시지 로그 저장하기 - 보수공사 후 진행 ->유저인포테이블
def userinfo_add(userinfo):

    json_data = {
        'id': userinfo.id,
        'user_id': userinfo.user_id,
        'image': userinfo.image
    }
    userinfo = add_all(json_data, userinfo.model)

    return userinfo

## GPT 정보 추가하기 & GPT 정보 업데이트하기 -> 챗봇테이블
def chatbot_add(chatbot):

    json_data = {
        'id': chatbot.id,
        'name': chatbot.name,
        'ai_id': chatbot.ai_id
    }
    chatbot = add_all(json_data, chatbot.model)

    return chatbot



#나
##-ChatStatistics
## 챗봇 대화 정보 저장하기 & 챗봇 대화 정보 업데이트하기 -
## 엔드타임 생성 & 엔드타임 생성에 필요한 정보 주는 함수 - 테스트코드 없음
## 엔드타임 업데이트 - 테스트코드 참고

def ChatStatistics_add(ChatStatistics):
    json_data = {
        "id" : ChatStatistics.id,
        'chatroom_id' : ChatStatistics.chatroom_id
    }
    ChatStatistics = add_all(json_data, ChatStatistics.model)

    return ChatStatistics




def ruser(User, Userinfo, AI, chatbot, chatroom, chatStatitics, db):
    print(f"ruser: ", "dfsdf")
    user_add(User, db)
    userinfo_add(Userinfo)
    ai_add(AI)
    chatbot_add(chatbot)
    chatroom_add(chatroom)
    ChatStatistics_add(chatStatitics)
        


def ruser_add(User, Userinfo, AI, chatbot, chatroom, chatStatitics):
    user_add(User)
    userinfo_add(Userinfo)
    ai_add(AI)
    chatbot_add(chatbot)
    chatroom_add(chatroom)
    ChatStatistics_add(chatStatitics)



