import json
import pprint



def get_ai(AI):
    # 객체에서 필요한 데이터만 추출
    usage = AI.usage
    message = AI.choices[0].message
    ai_speech_log = f'["{message.content}"]'

    
    new_ai = {
        'name': AI.id,
        'initial_prompt': AI.choices[0].message.role,
        'max_tokens': 500,  # 이 부분은 필요시 수정
        'prompt_tokens': usage.prompt_tokens,
        'completion_tokens': usage.completion_tokens,
        'total_tokens': usage.total_tokens,
        'ai_speech_log': ai_speech_log
    }
    
    # JSON 변환
    new_ai_json = json.dumps(new_ai)

    
    return new_ai

def get_user(user):
    
    new_user =  {
        'contact_info': None,
        'friend_status': user['friend_status'],
        'user_speech_log': f'["{user['user_speech_log']}"]'
        }
    
    return new_user

def get_chatbot(chatbot_name, ai_id):
    new_chatbot = {
        'name': chatbot_name,
        'ai_id': ai_id
        }
    
    return new_chatbot

def get_chat_statistics(chatroom_id):
    chat_statistics = {
        'chatroom_id': chatroom_id
        }
    
    return chat_statistics

def get_userinfo(userinfo):
    userinfo = {
        'user_id': userinfo['user_id'],
        'image': userinfo['image'],
        }
    
    return userinfo

def get_chatroom(user_id, ai_id,chatbot_id):
    chatroom = {
            'user_id': user_id,
            'ai_id': ai_id,
            'chatbot_id': chatbot_id
        }
    
    return chatroom


def update_ai(AI_id,AI):
    # 객체에서 필요한 데이터만 추출

    usage = AI.usage
    message = AI.choices[0].message
    ai_speech_log = f'["{message.content}"]'

    new_ai = {
        'id' : AI_id,
        'name': AI.id,
        'initial_prompt': AI.choices[0].message.role,
        'max_tokens': 500,  # 이 부분은 필요시 수정
        'prompt_tokens': usage.prompt_tokens,
        'completion_tokens': usage.completion_tokens,
        'total_tokens': usage.total_tokens,
        'ai_speech_log': ai_speech_log
    }
    
    # JSON 변환
    new_ai_json = json.dumps(new_ai)
    print("is_json", new_ai_json)
    
    return new_ai


def update_user(user_id, user):
    
    new_user =  {
        'id' : user_id,
        'contact_info': None,
        'friend_status': user['friend_status'],
        'user_speech_log': f'["{user['user_speech_log']}"]'
        }
    
    return new_user

def update_chatbot(id, ai_id):
    new_chatbot = {
        'id' : id,
        # 'name': chatbot_name,
        'ai_id': ai_id
        }
    
    return new_chatbot

def update_chat_statistics(id, chatroom_id):
    chat_statistics = {
        'id' : id,
        'chatroom_id': chatroom_id
        }
    
    return chat_statistics

def update_userinfo(userinfo):
    userinfo = {
        'id' : userinfo['id'],
        'user_id': userinfo['user_id'],
        'image': userinfo['image'],
        }
    
    return userinfo

def update_chatroom(id, user_id, ai_id,chatbot_id):
    chatroom = {
        'id' : id,
        'user_id': user_id,
        'ai_id': ai_id,
        'chatbot_id': chatbot_id
        }
    
    return chatroom