import copy
import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from openai import OpenAI
import uvicorn

from service.service import get_gpt_response, chatroom_add
from utils.utils import create_kakao_response

# from utils.utils import add_history, create_kakao_response


# .env 파일에서 환경 변수를 로드합니다.
load_dotenv()

# OpenAI 클라이언트 인스턴스를 생성합니다.
client = OpenAI()
app = FastAPI()

talk_history = []

# OpenAI 클라이언트 API 키를 설정합니다.
client.api_key = os.getenv('OPENAI_API_KEY')
print("OpenAI API Key:", client.api_key)

@app.get("/")
async def root():
    return {"message": "Hello World"}



@app.post("/chat")
async def chat(chat_request: Request):
    try:
        # 요청으로부터 JSON 데이터를 비동기적으로 가져옵니다.
        user_message = await chat_request.json()
        print(f"User message: {user_message}")
        
        message = user_message.get('userRequest', {}).get('utterance')
        # 만약 'message' 값이 없으면 예외를 발생시킵니다.
        if not message:
            raise ValueError("Message (utterance) key is missing in the request data.")
        # 대화 내역에 사용자의 메시지를 추가합니다.
        add_history(talk_history,"user",message)
        # OpenAI API에 요청을 보냅니다.
        gpt_message = get_gpt_response(client, message)
        # 최종적으로 클라이언트에게 응답을 반환합니다.
        print(f"Received response from OpenAI API: {gpt_message}")
        # 대화 내역에 OpenAI의 응답을 추가합니다.
        add_history(talk_history,"assistant", gpt_message)
        kakao_response = create_kakao_response(gpt_message)
    

        # 추가
        # # chatroom_add 함수를 호출하여 채팅방 정보를 저장하거나 업데이트합니다.
        chatroom_add()



        return JSONResponse(content=kakao_response)
    

    
    except Exception as e:
        # 오류가 발생할 경우, 콘솔에 오류를 출력하고 500 상태 코드를 반환합니다.
        print(f"OpenAI API request failed: {str(e)}")
        raise HTTPException(status_code=500, detail="OpenAI API request failed")


def add_history(talk_history, role, message):
    talk_history.append({"role": role, "content": message})
    return talk_history
    
if __name__ == '__main__':
    # Uvicorn을 사용하여 FastAPI 애플리케이션을 실행합니다.
    uvicorn.run(app, host='0.0.0.0', port=5000)
