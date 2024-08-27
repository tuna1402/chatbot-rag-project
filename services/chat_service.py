# services/chat_service.py
from openai import OpenAI
import os
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from repositories.chat_repository import save_chat_history
from datetime import datetime

# .env 파일에서 환경 변수 로드
load_dotenv()

# OpenAI 클라이언트 초기화
client = OpenAI()
client.api_key = os.getenv('OPENAI_API_KEY')

talk_history = []

def handle_chat(user_message: dict, db: Session):
    try:
        talk_history.append({"role": "user", "content": user_message['message']})
        
        if user_message:
            # OpenAI API에 메시지 전송
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=talk_history
            )
            
            gpt_message = response.choices[0].message.content
            talk_history.append({"role": "assistant", "content": gpt_message})

            # 대화 기록을 데이터베이스에 저장 (선택 사항)
            start_time = datetime.now()
            end_time = datetime.now()  # 실제 대화 종료 시간을 기록
            duration = end_time - start_time
            
            save_chat_history(db, user_message['user_id'], start_time, end_time, duration)
            
            return gpt_message
        else:
            raise ValueError("No message provided")
    except Exception as e:
        print(f"OpenAI API request failed: {str(e)}")
        raise Exception("OpenAI API request failed")
