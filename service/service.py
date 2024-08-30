from http import client
import pprint

from openai import OpenAI
from repository.database import add_all, db_session
from utils.utils import create_kakao_response


# 대화 내역을 저장할 리스트입니다.
talk_history = []

def get_gpt_response(client: OpenAI, message):
    response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": message}
                      ],
            max_tokens = 150,
            temperature = 0.7,
            talk_history = (add_all, chatroom_add)
        )

        # OpenAI로부터 받은 응답 메시지를 추출합니다.
    gpt_message = response.choices[0].message.content
    print(gpt_message)
    return gpt_message


def service_test():
    chatroom_add()
    pass






## 채팅방 추가하기 & 채팅방 업데이트하기
def chatroom_add(id, user_id, ai_id, chatbot_id, username, preferences, location, device):
    
    json_data = {
        'id': id,
        'user_id': user_id,
        'ai_id': ai_id,
        'chatbot_id': chatbot_id,
        
        # 여기에 추가 정보를 포함시킵니다.
        'additional_info': {
            'user_context': {
                'username': username,
                'preferences': preferences
            },
            'session_details': {
                'location': location,
                'device': device
            }
        }
    }        
    # 메모리에서의 값을 print로 출력합니다.
    print(f"id: {id}")
    print(f"user_id: {user_id}")
    print(f"ai_id: {ai_id}")
    print(f"chatbot_id: {chatbot_id}")
    print(f"Username: {username}")
    print(f"Preferences: {preferences}")
    print(f"Location: {location}")
    print(f"Device: {device}")
        
    
    chatroom = add_all(json_data, 'Chatroom')
    return chatroom


#지훈님
    ## AI 봇 추가하기 & AI 봇 업데이트하기 - 테이블 -> AI

def AI_add(id, name, initial_prompt, max_tokens, prompt_tokens, completion_tokens, total_tokens, ai_speech_log):
    # AI 봇 추가 또는 업데이트 테스트
    json_data = {
        'id': id,
        'name': name,
        'initial_prompt': initial_prompt,
        'max_tokens': max_tokens,
        'prompt_tokens': prompt_tokens,
        'completion_tokens': completion_tokens,
        'total_tokens': total_tokens,
        'ai_speech_log': ai_speech_log
    }


    AI = add_all(json_data, 'AI')

    ## 사용자 정보 추가하기 & 사용자 정보 업데이트하기 - 유저테이블
def User_add(id, contact_info, friend_status, user_speech_log):
    json_data = {
        'id': id,
        'contact_info': contact_info,
        'friend_status': friend_status,
        'user_speech_log': user_speech_log
    }

    User = add_all(json_data, 'User')

    




#다인님
## 사용자 메시지 로그 저장하기 - 보수공사 후 진행 ->유저인포테이블
## GPT 정보 추가하기 & GPT 정보 업데이트하기 -> 챗봇테이블

#나
##-ChatStatistics
## 챗봇 대화 정보 저장하기 & 챗봇 대화 정보 업데이트하기 -
## 엔드타임 생성 & 엔드타임 생성에 필요한 정보 주는 함수 - 테스트코드 없음
## 엔드타임 업데이트 - 테스트코드 참고


