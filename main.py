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



from models.get_data import get_ai, get_user, update_ai, update_user
from models.get_data import get_chat_statistics, get_chatbot, get_chatroom, get_userinfo
from models.talk_history import ChatRoom
from repository.database import db_session
from service.service import get_gpt_response, ruser ,ruser_update
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
    
    # 요청으로부터 JSON 데이터를 비동기적으로 가져옵니다.
        user_response = await chat_request.json()
        message = user_response.get('userRequest', {}).get('utterance')

        # 카카오톡 응답에서 필요한 값 추출
        chatroom_id = user_response.get('userRequest', {}).get('block', {}).get('id')
        chatroom_id2 = user_response.get('userRequest', {}).get('block', {}).get('id')

        ai_id = user_response.get('bot', {}).get('id')

        user_id = user_response.get('userRequest', {}).get('user', {}).get('id')

        is_friend = user_response.get('userRequest', {}).get('user', {}).get('properties', {}).get('isFriend')
        user_message = user_response.get('userRequest', {}).get('utterance', {})
        
        chatbot_name = user_response.get('bot', {}).get('id')
        
        def to_get_user(is_friend,user_message):
            user =  {
                'friend_status': is_friend,
                'user_speech_log': user_message
                }
            print("친구친구",is_friend)
            print("친구친구",user_message)
            
            return user
        
        
        new_user = to_get_user(is_friend, user_message)
        
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
        gpt_all = get_gpt_response(client, message)
        
        gpt_response = gpt_all.choices[0].message.content
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
        print("gpt 리스폰스",gpt_all)
        print("ai 시작", gpt_all)
        AI = get_ai(gpt_all)
        print("aaaaaa", AI)
        
        user = get_user(new_user)
        
        new_chatbot = chatbot_name
        
        if user_id not in chat_history:
            # 기존 데이터를 생성합니다.
            new_chatroom = ruser(user, AI, new_chatbot, db)
            # 각 채팅방에 메시지를 추가 (생성 직후)
            new_chatroom.add_message({"role":"user", "content": message})
            
            new_chatroom.add_message({"role":"assistant", "content": gpt_response})
            
            print("history : ", new_chatroom.get_chat_history())
            chat_history[user_id] = new_chatroom
            print("history : ", chat_history[user_id])
        else:      
            # 사용자 존재를 확인 후 업데이트를 진행한다.
            for history_user_id, chat_room in chat_history.items():
                print("user_id, chat_room : ",user_id, chat_room)
                if(history_user_id == user_id):
                    room:ChatRoom = chat_history[user_id]
                    user = update_user(room.get_user_id(), new_user);
                    update_AI = update_ai(room.get_ai_id(), gpt_all)
                    # ruser_update(user, AI, db)
                    room.add_message({"role":"user", "content": message})
                    room.add_message({"role":"assistant", "content": gpt_response})
                    ruser_update(user, update_AI ,db, room)
                    print("history : ", room.get_chat_history())

    

        

        return JSONResponse(content=kakao_response)
    
    # try:
        

    # except Exception as e:
    #     # 오류가 발생할 경우, 콘솔에 오류를 출력하고 500 상태 코드를 반환합니다.
    #     print(f"Chat 엔드포인트 내의 에러: {str(e)}")
    #     raise HTTPException(status_code=500, detail=str(e) if not isinstance(e, set) else list(e))




def add_history(talk_history, role, message):
    talk_history.append({"role": role, "content": message})
    return talk_history
    
if __name__ == '__main__':
    # Uvicorn을 사용하여 FastAPI 애플리케이션을 실행합니다.
    uvicorn.run(app, host='0.0.0.0', port=5000)
