import copy
import os
from typing import List
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, Request
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from openai import OpenAI
import uvicorn
from models.dto import gpt_message 



from models.dummy import get_ai, get_user
from models.talk_history import ChatRoom
from repository.database import db_session
from service.service import get_gpt_response, ruser, ruser_update
from utils.utils import create_kakao_response

# from utils.utils import add_history, create_kakao_response


# .env 파일에서 환경 변수를 로드합니다.
load_dotenv()

# OpenAI 클라이언트 인스턴스를 생성합니다.
client = OpenAI()
app = FastAPI()

chat_history = {}
talk_history = []
send_to_rag = []

# OpenAI 클라이언트 API 키를 설정합니다.
client.api_key = os.getenv('OPENAI_API_KEY')
print("OpenAI API Key:", client.api_key)


@app.post("/chat")
async def chat(chat_request: Request, db: Session = Depends(db_session)):
    try:
        # 요청으로부터 JSON 데이터를 비동기적으로 가져옵니다.
        user_message = await chat_request.json()
        
        message = user_message.get('userRequest', {}).get('utterance')

        # 카카오톡 응답에서 필요한 값 추출
        chatroom_id = user_message.get('userRequest', {}).get('block', {}).get('id')
        ai_id = user_message.get('bot', {}).get('id')
        user_id = user_message.get('userRequest', {}).get('user', {}).get('id')
        
        
        
        # send to rag -> 코드 내에서 생성되는 값을 가져옴
        # 챗룸아이디 : ChatRoom_id
        # user id  : User.id
        # ai id : AI.id
        # bot id : Chatbot.id
        # messages: {role, message}

        
        # 추출한 값이 None이면 예외 발생
        if not all([chatroom_id, ai_id, user_id]):
            raise ValueError("chatroom_id, ai_id, or user_id is missing in the request data.")
        
        
        # 만약 'message' 값이 없으면 예외를 발생시킵니다.
        if not message:
            raise ValueError("Message (utterance) key is missing in the request data.")
        
        #send_to_rag 를 위한 카카오msg
        # user_msg = gpt_message(role = 'user' , content = message)
        #user_msg: gpt_message = { "role":"user", "content":message }
        #send_to_rag.append(user_msg)
        
        
        # 대화 내역에 사용자의 메시지를 추가합니다.
        add_history(talk_history,"user",message)
        
        # OpenAI API에 요청을 보냅니다.
        # gpt_message = get_gpt_response(client, message)
        gpt_response = get_gpt_response(client, message)
        
        
        #send_to_rag 를 위한 gpt_msg
        # gpt_msg = gpt_message(role='assistant', content=gpt_response)
         #send_to_rag 를 위한 gpt_msg
         
        gpt_msg: gpt_message = { "role":"user", "content":message }
        
        send_to_rag.append(gpt_msg)
        
        
        # 최종적으로 클라이언트에게 응답을 반환합니다.
        
        # 대화 내역에 OpenAI의 응답을 추가합니다.
        add_history(talk_history,"assistant", gpt_response)
        kakao_response = create_kakao_response(gpt_response)
    
        print("Current send_to_rag contents:", gpt_response)
        print("send to rag", send_to_rag)

        print("user_add", )


        # 추가
        # # chatroom_add 함수를 호출하여 채팅방 정보를 저장하거나 업데이트합니다.
        
        
        AI = get_ai()
        
        
        user = get_user()
        
        chatbot = {
        'id': 1,
        'name': 'Test Chatbot',
        'ai_id': 1
        }

        chatroom = {
            'id': 1,
            'user_id': 1,
            'ai_id': 1,
            'chatbot_id': 1,
            'username': 'user',
            'preferences': 'preferences',
            'location': 'location',
            'device': 'device'
        }
        
        # gpt_message = {
        #     "role" : "role a",
        #     'content' : 'content a',
        # }
        
        
        
        userinfo = {
        'id': 1,
        'user_id': 1,
        'image': 'image.png',
        }        
        
        chat_statistics = {
        'id': 1,
        'chatroom_id': 1
        }
        
        if kakao not in chat_history:
            # 기존 데이터를 생성합니다.
            new_chatroom = ruser(user, userinfo, AI, chatbot, chatroom, chat_statistics, db)
            # 각 채팅방에 메시지를 추가 (생성 직후)
            new_chatroom.add_message({"role":"user", "content": message})
            new_chatroom.add_message({"role":"assistant", "content": gpt_response})
            
            print("history : ", new_chatroom.get_chat_history())
            chat_history["user_id"] = new_chatroom
            print("history : ", chat_history["user_id"])
    
         
        ## 사용자 존재를 확인 후 업데이트를 진행한다.
        for history_user_id, chat_room in chat_history.items():
            print("user_id, chat_room : ",user_id, chat_room)
            if(history_user_id == "user_id"):
                room:ChatRoom = chat_history["user_id"]
                ruser_update(user, userinfo, AI, chatbot, chatroom, chat_statistics, db)
                room.add_message({"role":"user", "content": message})
                room.add_message({"role":"assistant", "content": gpt_response})
                print("history : ", room.get_chat_history())

    
        new_user = (user, userinfo, AI, chatbot, chatroom, chat_statistics, db)
    
        

        return JSONResponse(content=kakao_response)

    except Exception as e:
        # 오류가 발생할 경우, 콘솔에 오류를 출력하고 500 상태 코드를 반환합니다.
        print(f"Chat 엔드포인트 내의 에러: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e) if not isinstance(e, set) else list(e))


def add_history(talk_history, role, message):
    talk_history.append({"role": role, "content": message})
    return talk_history
    
if __name__ == '__main__':
    # Uvicorn을 사용하여 FastAPI 애플리케이션을 실행합니다.
    uvicorn.run(app, host='0.0.0.0', port=5000)
