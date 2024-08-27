import json
from base import SessionLocal, Base, engine
from datetime import datetime, timedelta
from models import AI, User, Chatbot, ChatRoom, UserInfo, ChatStatistics
from datetime import datetime


last_chat_time = None

def last_chat_log_time():
    global last_chat_time  # 전역변수를 사용하기 위해 선언
    last_chat_time = datetime.now()

def get_last_chat_log_time():
    return last_chat_time

# create&update


# add_all
def add_all(json_data: dict, model_name: str):

    # model_name에 따라 함수를 호출합니다.
    if model_name == 'AI':
        return ai_add_or_update_data(json_data)
    elif model_name == 'User':
        return user_add_or_update_data(json_data)
    elif model_name == 'Chatbot':
        return chatbot_add_data(json_data)
    elif model_name == 'ChatRoom':
        return chatroom_add_data(json_data)
    elif model_name == 'UserInfo':
        return userinfo_add_or_update_data(json_data)
    elif model_name == 'ChatStatistics':
        return chat_statistics_add_or_update_data(json_data)

# ai_add_data
def ai_add_or_update_data(json_data: dict):

    # Json 데이터를 파싱합니다.
    ai_id = json_data.get('id')
    name = json_data.get('name')
    initial_prompt = json_data.get('initial_prompt')
    max_tokens = json_data.get('max_tokens')
    usage_data = {
            "prompt_tokens": json_data.get('prompt_tokens', 0),
            "completion_tokens": json_data.get('completion_tokens', 0),
            "total_tokens": json_data.get('total_tokens', 0)
    }
    ai_speech_log = json_data.get('ai_speech_log', '[]')
    
    with SessionLocal() as db:
        ai = db.query(AI).filter(AI.id == ai_id).first()

        # 기존 ai 데이터를 업데이트합니다.
        if ai:
            ai.name = name
            ai.initial_prompt = initial_prompt
            ai.max_tokens = max_tokens
            existing_usage = json.loads(ai.usage) if ai.usage else {}
            existing_usage.update(usage_data)
            ai.usage = json.dumps(existing_usage, ensure_ascii=False)
            
            # ai_speech_log룰 업데이트합니다. (기존 데이터에 추가)
            log_list = json.loads(ai.ai_speech_log)
            new_log_list = json.loads(ai_speech_log)
            log_list.extend(new_log_list)
            ai.ai_speech_log = json.dumps(log_list, ensure_ascii=False)
        
        # ai(id)가 존재하지 않을 경우 새 ai를 추가합니다.
        else:
            ai = AI(
                id=ai_id,
                name=name,
                initial_prompt=initial_prompt,
                max_tokens=max_tokens,
                usage=json.dumps(usage_data, ensure_ascii=False),
                ai_speech_log=json.dumps(json.loads(ai_speech_log), ensure_ascii=False)
            )
            db.add(ai)
        
        db.commit()  # 변경 사항 저장
        db.refresh(ai)  # 세션 새로고침

        
        return ai

# user_add_data
def user_add_or_update_data(json_data: dict):

    user_id = json_data.get('id')
    contact_info = json_data.get('contact_info')
    friend_status = json_data.get('friend_status')
    revisit_count = json_data.get('revisit_count')
    user_speech_log = json_data.get('user_speech_log', '[]')

    with SessionLocal() as db:

        user = db.query(User).filter(User.id == user_id).first()
        
        # 기존 사용자 데이터를 업데이트합니다.
        if user:
            user.contact_info = contact_info
            user.friend_status = friend_status
            revisit_count = revisit_count
            chat_list = json.loads(user.user_speech_log)
            new_chat_list = json.loads(user_speech_log)
            chat_list.extend(new_chat_list)
            user.user_speech_log = json.dumps(chat_list, ensure_ascii=False)

        # 사용자(id)가 존재하지 않을 경우 새 사용자를 추가합니다.
        else:
            user = User(
                id=user_id,
                contact_info=contact_info,
                friend_status=friend_status,
                revisit_count=revisit_count,
                user_speech_log=json.dumps(json.loads(user_speech_log), ensure_ascii=False)
            )
            db.add(user)
        
        db.commit()
        db.refresh(user)
        return user

# chatbot_add_data
def chatbot_add_data(json_data: dict):
    chatbot_id = json_data.get('id')
    name = json_data.get('name')
    ai_id = json_data.get('ai_id')

    with SessionLocal() as db:
        chatbot = Chatbot(
            id=chatbot_id,
            name=name,
            ai_id=ai_id
        )
        
        db.add(chatbot)
        db.commit()
        db.refresh(chatbot)
        
        last_chat_log_time()

        return chatbot
    
# chatroom_add_data
def chatroom_add_data(json_data: dict):
    chatroom_id = json_data.get('id')
    user_id = json_data.get('user_id')
    ai_id = json_data.get('ai_id')
    chatbot_id = json_data.get('chatbot_id')
    start_time = datetime.fromisoformat(json_data.get('start_time'))
    
    with SessionLocal() as db:

        existing_chatroom = db.query(ChatRoom).filter(ChatRoom.id == chatroom_id).first()
        
        if existing_chatroom:
            end_time = existing_chatroom.end_time

            if end_time:
                # end_time이 존재하는 경우 conversation_duration 계산
                conversation_duration = end_time - start_time
            else:
                # end_time이 존재하지 않는 경우, conversation_duration은 None
                conversation_duration = None

            # 기존 ChatRoom을 업데이트합니다.
            existing_chatroom.user_id = user_id
            existing_chatroom.ai_id = ai_id
            existing_chatroom.chatbot_id = chatbot_id
            existing_chatroom.start_time = start_time
            existing_chatroom.end_time = end_time
            existing_chatroom.conversation_duration = conversation_duration

            db.commit()  # 변경 사항을 커밋합니다.
            db.refresh(existing_chatroom)
            
            return existing_chatroom

        else:
            # 기존 ChatRoom이 존재하지 않는 경우 새로 생성합니다.
            chatroom = ChatRoom(
                id=chatroom_id,
                user_id=user_id,
                ai_id=ai_id,
                chatbot_id=chatbot_id,
                start_time=start_time,
                end_time=None,  # end_time은 NULL로 설정
                conversation_duration=None  # conversation_duration은 NULL로 설정
            )
            
            db.add(chatroom)
            db.commit()
            db.refresh(chatroom)
            
            return chatroom

# userInfo_add_data
def userinfo_add_or_update_data(json_data: dict):

    userinfo_id = json_data.get('id')
    user_id = json_data.get('user_id')
    image = json_data.get('image')
    trend_design = json_data.get('trend_design', '[]')
    budget = json_data.get('budget')
    age = json_data.get('age')
    region = json_data.get('region')

    with SessionLocal() as db:

        userinfo = db.query(UserInfo).filter(UserInfo.id == userinfo_id).first()

        # 기존 userinfo 데이터를 업데이트합니다.
        if userinfo:
            userinfo.user_id = user_id
            userinfo.image = image
            userinfo.budget = budget
            userinfo.age = age
            userinfo.region = region
            
            # trend_design 업데이트 (기존 디자인에 새 디자인 추가)
            trend_list = json.loads(userinfo.trend_design)
            new_trend_list = json.loads(trend_design)
            trend_list.extend(new_trend_list)
            userinfo.trend_design = json.dumps(trend_list, ensure_ascii=False)
            
        else:
            userinfo = UserInfo(
                id=userinfo_id,
                user_id=user_id,
                image=image,
                trend_design=json.dumps(json.loads(trend_design), ensure_ascii=False),
                budget=budget,
                age=age,
                region=region
            )
            db.add(userinfo)

        db.commit()
        db.refresh(userinfo)

        return userinfo

# chatStatistics_data
def chat_statistics_add_or_update_data(json_data: dict):
    
    statistics_id = json_data.get('id')
    chatroom_id = json_data.get('chatroom_id')
    average_chat_duration = timedelta(seconds=json_data.get('average_chat_duration'))

    average_tokens = json_data.get('average_tokens')

    with SessionLocal() as db:

        statistics = db.query(ChatStatistics).filter(ChatStatistics.id == statistics_id).first()

        if statistics:
            statistics.chatroom_id = chatroom_id
            statistics.average_chat_duration = average_chat_duration
            statistics.average_tokens = average_tokens
            
            # ChatRoom을 통해 AI의 id를 찾고, AI의 usage에서 total_tokens를 가져옵니다.
            chatroom = db.query(ChatRoom).filter(ChatRoom.id == chatroom_id).first()
            if chatroom:
                ai = db.query(AI).filter(AI.id == chatroom.ai_id).first()
                if ai:
                    existing_usage = json.loads(ai.usage) if ai.usage else {}
                    ai_total_tokens = existing_usage.get('total_tokens', 0)
                    
                    # 기존 total_tokens에 AI의 total_tokens 값을 추가합니다.
                    statistics.total_tokens = (statistics.total_tokens or 0) + ai_total_tokens

                # total_chat_duration를 업데이트합니다.
                if statistics.total_chat_duration:
                    if chatroom.conversation_duration:
                        statistics.total_chat_duration += chatroom.conversation_duration
                else:
                    if chatroom.conversation_duration:
                        statistics.total_chat_duration = chatroom.conversation_duration

        else:
            chatroom = db.query(ChatRoom).filter(ChatRoom.id == chatroom_id).first()
            if chatroom:
                ai = db.query(AI).filter(AI.id == chatroom.ai_id).first()
                if ai:
                    existing_usage = json.loads(ai.usage) if ai.usage else {}
                    ai_total_tokens = existing_usage.get('total_tokens', 0)
                    
                    # total_tokens를 새로 지정하고 AI의 total_tokens 값을 추가합니다.
                    total_tokens = ai_total_tokens
                
                otal_chat_duration = chatroom.conversation_duration or timedelta()
            else:
                total_tokens = 0
                total_chat_duration = None
            
            statistics = ChatStatistics(
                id=statistics_id,
                chatroom_id=chatroom_id,
                total_chat_duration=total_chat_duration,
                average_chat_duration=average_chat_duration,
                total_tokens=total_tokens,
                average_tokens=average_tokens
            )
            db.add(statistics)

        db.commit()
        db.refresh(statistics)

        return statistics


def update_end_time(json_data: dict):

    id = json_data.get('id')
    end_time = json_data.get('end_time')

    # end_time을 datetime 객체로 변환합니다.
    end_time = datetime.fromisoformat(end_time) if end_time else None

    with SessionLocal() as db:
        # 주어진 id로 ChatRoom을 조회합니다.
        chatroom = db.query(ChatRoom).filter(ChatRoom.id == id).first()
        
        if chatroom:
            chatroom.end_time = end_time
            db.commit()
        else:
            print("해당하는 id의 chatroom은 존재하지 않습니다.")


# read

# time_and_token_search
def time_and_token_search(chatroom_id: int):
    with SessionLocal() as session:

        # 현재 시간을 담을 변수
        current_time = datetime.now()

        # ChatRoom과 AI 테이블을 조인하여 end_time와 total_tokens를 가져옵니다.
        result = (
            session.query(ChatStatistics.total_tokens)
            .join(ChatStatistics, ChatRoom.id == ChatStatistics.chatroom_id)
            .filter(ChatRoom.id == chatroom_id)
            .first()
        )

        last_chat_time = get_last_chat_log_time()


        if result is None:
            return None

        total_tokens = result

        # 현재 시간, end_time, total_tokens를 반환합니다.
        return {
            "last_chat_time" : last_chat_time,
            "current_time": current_time,
            "total_tokens": total_tokens
        }