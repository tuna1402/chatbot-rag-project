import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from openai import OpenAI


# .env 파일에서 환경 변수를 로드합니다.
load_dotenv()

# OpenAI 클라이언트 인스턴스를 생성합니다.
client = OpenAI()
app = FastAPI()



# 대화 내역을 저장할 리스트입니다.
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

        # 'userRequest' 객체 내부의 'utterance' 값을 추출합니다.
        message = user_message.get('userRequest', {}).get('utterance')
        
        # 만약 'message' 값이 없으면 예외를 발생시킵니다.
        if not message:
            raise ValueError("Message (utterance) key is missing in the request data.")
        
        # 대화 내역에 사용자의 메시지를 추가합니다.
        talk_history.append({"role": "user", "content": message})
        
        # OpenAI API에 요청을 보냅니다.
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
        
        # 대화 내역에 OpenAI의 응답을 추가합니다.
        talk_history.append({"role": "assistant", "content": gpt_message})
        
        kakao_response = {
        "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                            "text": gpt_message
                        }
                    }
                ]
            }
        }
    
        #sleep(5)
        
        
        # 최종적으로 클라이언트에게 응답을 반환합니다.
        print(f"Received response from OpenAI API: {gpt_message}")
        return JSONResponse(content=kakao_response)
    

    
    except Exception as e:
        # 오류가 발생할 경우, 콘솔에 오류를 출력하고 500 상태 코드를 반환합니다.
        print(f"OpenAI API request failed: {str(e)}")
        raise HTTPException(status_code=500, detail="OpenAI API request failed")

    
if __name__ == '__main__':
    # Uvicorn을 사용하여 FastAPI 애플리케이션을 실행합니다.
    uvicorn.run(app, host='0.0.0.0', port=5000)
