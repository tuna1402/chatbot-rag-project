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
def chatroom_add():
    
    json_data = {
        'id': 1,
        'user_id': 1,
        'ai_id': 1,
        'chatbot_id': 1
    }
    chatroom = add_all(json_data, 'Chatroom')


#지훈님
## AI 봇 추가하기 & AI 봇 업데이트하기 - 테이블 -> AI
## 사용자 정보 추가하기 & 사용자 정보 업데이트하기 - 유저테이블


#다인님
## 사용자 메시지 로그 저장하기 - 보수공사 후 진행 ->유저인포테이블
## GPT 정보 추가하기 & GPT 정보 업데이트하기 -> 챗봇테이블

#나
##-ChatStatistics
## 챗봇 대화 정보 저장하기 & 챗봇 대화 정보 업데이트하기 -
## 엔드타임 생성 & 엔드타임 생성에 필요한 정보 주는 함수 - 테스트코드 없음
## 엔드타임 업데이트 - 테스트코드 참고


