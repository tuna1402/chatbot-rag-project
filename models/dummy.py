def get_ai():
    AI = {
        'id': 1,
        'name': "ai이름",
        'initial_prompt': 'Hello',
        'max_tokens': 1100,
        'prompt_tokens': 40,
        'completion_tokens': 30,
        'total_tokens': 70,
        'ai_speech_log': '["오늘 날씨 어떄?"]'
        }
    return AI

def get_user():
    user =  {
        'id': 2,
        'contact_info': 'test1@example.com',
        'friend_status': True,
        'user_speech_log': '["제가 원하는 디자인은 미니멀리즘 스타일입니다. 예산은 천만원 나이는 여든한살입니다. 현재 대구에 거주 중이에요."]'
        }
    
    return user