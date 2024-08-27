# repositories/chat_repository.py
from sqlalchemy.orm import Session
from models import ChatRoom

def save_chat_history(db: Session, user_id: int, start_time, end_time, duration):
    new_chat = ChatRoom(
        user_id=user_id,
        start_time=start_time,
        end_time=end_time,
        conversation_duration=duration
    )
    db.add(new_chat)
    db.commit()
    db.refresh(new_chat)
    return new_chat
