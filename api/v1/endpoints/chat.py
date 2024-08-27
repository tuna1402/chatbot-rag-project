# api/v1/endpoints/chat.py
from fastapi import APIRouter, HTTPException, Request, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from services.chat_service import handle_chat
from database import get_db

router = APIRouter()

@router.post("/chat")
async def chat(chat_request: Request, db: Session = Depends(get_db)):
    try:
        user_message = await chat_request.json()
        response = handle_chat(user_message, db)
        return JSONResponse(content={"response": response})
    except Exception as e:
        print(f"OpenAI API request failed: {str(e)}")
        raise HTTPException(status_code=500, detail="OpenAI API request failed")
