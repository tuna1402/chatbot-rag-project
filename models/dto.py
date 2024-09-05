from typing import List
from pydantic import BaseModel

#데이터 형식 정의

class AI_add_datatype(BaseModel):
    name : str
    initial_prompt : str
    max_tokens : int
    prompt_tokens : int
    completion_tokens : int
    total_tokens :  int
    ai_speech_log : str

class AI_update_datatype(BaseModel):
    id : int
    name : str
    initial_prompt : str
    max_tokens : int
    prompt_tokens : int
    completion_tokens : int
    total_tokens :  int
    ai_speech_log : str

class User_add_datatype(BaseModel):
    contact_info : str
    friend_status : bool
    revisit_count : int
    user_speech_log : str

class User_update_datatype(BaseModel):
    id : int
    contact_info : str
    friend_status : bool
    revisit_count : int
    user_speech_log : str

class UserInfo_add_datatype(BaseModel):
    user_id : int
    image : str



class UserInfo_update_datatype(BaseModel):
    id : int
    user_id : int
    image : str

# UserContext, SessionDetails 확인 후 수정 바람
class UserContext(BaseModel):
    username: str
    preferences: str

class SessionDetails(BaseModel):
    location: str
    device: str

class AdditionalInfo(BaseModel):
    user_context: UserContext
    session_details: SessionDetails

class Chatroom_add_datatype(BaseModel):
    user_id : int
    ai_id : int
    chatbot_id : int
    additional_info : AdditionalInfo

class Chatroom_update_datatype(BaseModel):
    id : int
    user_id : int
    ai_id : int
    chatbot_id : int
    additional_info : AdditionalInfo

class Chatbot_add_datatype(BaseModel):
    name : str
    ai_id : int

class Chatbot_update_datatype(BaseModel):
    id : int
    name : str
    ai_id : int

class ChatStatistics_add_datatype(BaseModel):
    chatroom_id : int

class ChatStatistics_update_datatype(BaseModel):
    id : int
    chatroom_id : int

class gpt_message (BaseModel):

    role : str
    content : str

class talk_history (BaseModel): 

    chatroom_id : str
    ai_id : str 
    user_id : int
    gpt_message : List[gpt_message]
