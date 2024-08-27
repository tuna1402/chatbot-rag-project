from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from openai import OpenAI
import os
from dotenv import load_dotenv
from fastapi.responses import JSONResponse
import json

load_dotenv()
client = OpenAI()

app = FastAPI()

talk_history = []


# OpenAI 클라이언트 설정
client.api_key = os.getenv('OPENAI_API_KEY')
print("OpenAI API Key:", client.api_key)
print("API Key:", client.api_key)

@app.get("/")
def root():
    return{'hello' : 'world!'}


@app.post("/chat")
async def chat(chat_request: Request):
    try:
        
        user_message = await chat_request.json()
        print(f"User message: {user_message}")
        talk_history.append({"role": "user", "content": user_message['message']})

        
        if user_message:
            # print(f"Attempting to send request to OpenAI API with message: {user_message}")
            response = client.chat.completions.create(
                
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": user_message['message']}]
                # messages = talk_history
            )
    
            gpt_message = response.choices[0].message.content
            print(gpt_message)
                    
            {
                "version": "2.0",
                "useCallback": True,
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
            
            # print(type(response.choices[0].message.content))
            
            
            talk_history.append({"role": "assistant", "content": gpt_message})

            print(f"Received response from OpenAI API: {gpt_message}")
            return JSONResponse(content={"response": gpt_message})
        else:
            raise HTTPException(status_code=400, detail="No message provided")
    except Exception as e:
        print(f"OpenAI API request failed: {str(e)}")
        raise HTTPException(status_code=500, detail="OpenAI API request failed")

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=5000)
