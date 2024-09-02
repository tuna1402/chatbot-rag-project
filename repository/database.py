import json
from fastapi import Depends
from sqlalchemy import func
from repository.base import SessionLocal, Base, engine
from utils import db_util
from datetime import datetime, timedelta
from models.models import AI, User, Chatbot, ChatRoom, UserInfo, ChatStatistics
from sqlalchemy.orm import Session


# last_chat_log_time() 함수를 호출한 시간을 마지막 채팅 시간(last_chat_time)으로 저장합니다.
# get_last_chat_log_time() 함수를 호출할 시 마지막 채팅 시간을 return합니다.

# add_all() model_name 값에 해당하는 함수를 호출하며 매개변수로 json_data를 전달합니다.

# ai_add_or_update_data 전달받은 매개변수의 데이터를 ai 엔티티에 추가하거나 업데이트합니다.
# user_add_or_update_data 전달받은 매개변수의 데이터를 users 엔티티에 추가하거나 업데이트합니다.
# chatbot_add_or_update_data 전달받은 매개변수의 데이터를 chatbot 엔티티에 추가하거나 업데이트합니다.
# chatroom_add_or_update 전달받은 매개변수의 데이터를 chatroom 엔티티에 추가하거나 업데이트합니다.
# userInfo_add_data 전달받은 매개변수의 데이터를 user_info 엔티티에 추가하거나 업데이트합니다.
# chatStatistics_data 전달받은 매개변수의 데이터를 chat_statistics 엔티티에 추가하거나 업데이트합니다.

# update_end_time() 채팅이 종료되었을 때 end_time를 업데이트합니다.
# time_and_token_search() 호출 시 마지막 채팅 시간, 현재 시간, total_token값을 반환합니다.

last_chat_time = None

def db_session():
    # 새로운 데이터베이스 세션을 생성합니다.
    connection = engine.connect()
    transaction = connection.begin()
    session = SessionLocal(bind=connection)
    
    try:
        yield session
        transaction.commit()  # 성공적으로 수행된 경우 커밋
    except Exception:
        transaction.rollback()  # 예외 발생 시 롤백
        raise  # 예외를 다시 발생시켜 호출자가 처리할 수 있게 함
    finally:
        session.close()  # 세션 종료
        connection.close()  # 연결 종료

def last_chat_log_time():
    global last_chat_time
    last_chat_time = datetime.now()

def get_last_chat_log_time():
    return last_chat_time


# create&update

def add_all(json_data: dict, model_name: str, db: Session):
    
    # model_name에 따라 함수를 호출합니다.
    if model_name == 'AI':
        return ai_add_or_update_data(json_data, db)
    elif model_name == 'User':
        return user_add_or_update_data(json_data, db)
    elif model_name == 'Chatbot':
        return chatbot_add_or_update_data(json_data, db)
    elif model_name == 'ChatRoom':
        return chatroom_add_or_update(json_data, db)
    elif model_name == 'UserInfo':
        return userinfo_add_or_update_data(json_data, db)
    elif model_name == 'ChatStatistics':
        return chat_statistics_add_or_update_data(json_data, db)

def ai_add_or_update_data(json_data: dict, db: Session):
    db_session()
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
            
            # ai_speech_log를 업데이트합니다. (기존 데이터에 추가)
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

def user_add_or_update_data(json_data: dict, db: Session):

    user_id = json_data.get('id')
    contact_info = json_data.get('contact_info')
    friend_status = json_data.get('friend_status')
    user_speech_log = json_data.get('user_speech_log', '[]')

    with SessionLocal() as db:
        user = db.query(User).filter(User.id == user_id).first()
        
        # 기존 사용자 데이터를 업데이트합니다.
        if user:
            user.contact_info = contact_info
            user.friend_status = friend_status
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
                revisit_count=0,
                user_speech_log=json.dumps(json.loads(user_speech_log), ensure_ascii=False)
            )
            db.add(user)
        
        db.commit()
        db.refresh(user)

        return user

def chatbot_add_or_update_data(json_data: dict, db: Session):
    chatbot_id = json_data.get('id')
    name = json_data.get('name')
    ai_id = json_data.get('ai_id')

    with SessionLocal() as db:
        chatbot = db.query(Chatbot).filter(Chatbot.id == chatbot_id).first()

        # 기존 사용자 데이터를 업데이트합니다.
        if chatbot:
            chatbot.name = name
            chatbot.ai_id = ai_id
        else:

            # 챗봇이(id) 존재하지 않을 경우 새 챗봇을 추가합니다.
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
    
def chatroom_add_or_update(json_data: dict, db: Session):
    chatroom_id = json_data.get('id')
    user_id = json_data.get('user_id')
    ai_id = json_data.get('ai_id')
    chatbot_id = json_data.get('chatbot_id')
    
    with SessionLocal() as db:
        existing_chatroom = db.query(ChatRoom).filter(ChatRoom.id == chatroom_id).first()
         
        if existing_chatroom:
            end_time = existing_chatroom.end_time

            if end_time:
                existing_chatroom.start_time = datetime.utcnow()  # 현재 시간으로 start_time을 업데이트합니다.
                existing_chatroom.end_time = None  # end_time을 초기화합니다.
                existing_chatroom.conversation_duration = None
            else:
                # end_time이 존재하지 않으면(=채팅이 종료되지 않았다면) start_time과 conversation_duration을 그대로 유지합니다.
                pass

            # user_id, ai_id, chatbot_id를 업데이트합니다.
            existing_chatroom.user_id = user_id
            existing_chatroom.ai_id = ai_id
            existing_chatroom.chatbot_id = chatbot_id

            # User의 revisit_count를 업데이트합니다.
            user = db.query(User).filter(User.id == user_id).first()
            if user:
                user.revisit_count = (user.revisit_count or 0) + 1

            db.commit()
            db.refresh(existing_chatroom)

            return existing_chatroom
        
        # 채팅방이(id) 존재하지 않을 경우 새 채팅방을 추가합니다.
        else:
            chatroom = ChatRoom(
                id=chatroom_id,
                user_id=user_id,
                ai_id=ai_id,
                chatbot_id=chatbot_id,
                start_time=datetime.utcnow(),  # 처음 생성 시 현재 시간으로 start_time 설정합니다.
                end_time=None,  # 초기 end_time은 None로 설정합니다.
                conversation_duration=timedelta(0)
            )
            
            db.add(chatroom)
            db.commit()
            db.refresh(chatroom)

            return chatroom

def userinfo_add_or_update_data(json_data: dict, db: Session):

    userinfo_id = json_data.get('id')
    user_id = json_data.get('user_id')
    image = json_data.get('image', '') 

    with SessionLocal() as db:
        # userinfo를 조회합니다.
        userinfo = db.query(UserInfo).filter(UserInfo.id == userinfo_id).first()
        
        # user_speech_log에서 가장 최근의 로그 항목을 조회합니다.
        user = db.query(User).filter(User.id == user_id).first()
        if user and user.user_speech_log:
            user_speech_log = json.loads(user.user_speech_log)
            last_log_text = user_speech_log[-1] if user_speech_log else ""
            
            # util.py의 함수를 통해 스타일, 예산, 나이, 지역 정보를 추출합니다.
            extracted_style = db_util.extract_style(last_log_text)
            extracted_budget = db_util.extract_budget(last_log_text)
            extracted_age = db_util.extract_age(last_log_text)
            extracted_region = db_util.extract_city(last_log_text)
        else:
            extracted_style = "None"
            extracted_budget = "None"
            extracted_age = "None"
            extracted_region = "None"

        # userinfo 데이터를 업데이트 또는 추가합니다.
        if userinfo:
            userinfo.user_id = user_id

            # image 업데이트: 빈 문자열이면 None으로 처리합니다.
            if image == "":
                userinfo.image = None
            else:
                userinfo.image = image

            # trend_design 업데이트: 기존 데이터에 새로 추출한 스타일을 추가합니다.
            if extracted_style != "None":
                existing_trend_list = json.loads(userinfo.trend_design) if userinfo.trend_design else []
                
                # extracted_style이 문자열인 경우 리스트로 변환
                if isinstance(extracted_style, str):
                    extracted_style = [extracted_style]
                
                # 중복 제거
                new_trend_list = list(set(existing_trend_list + extracted_style))  # 중복 제거
                userinfo.trend_design = json.dumps(new_trend_list, ensure_ascii=False)
            
            # 예산을 업데이트합니다.
            if extracted_budget != "None":
                userinfo.budget = extracted_budget
            
            # 나이를 업데이트합니다.
            if extracted_age != "None":
                userinfo.age = extracted_age
            
            # 지역을 업데이트합니다.
            if extracted_region != "None":
                userinfo.region = extracted_region

        # 유저 정보가(id) 존재하지 않을 경우 새 유저 정보를 추가합니다. 
        else:
            userinfo = UserInfo(
                id=userinfo_id,
                user_id=user_id,
                image=None if image == "" else image,
                trend_design=json.dumps([extracted_style] if extracted_style != "None" else [], ensure_ascii=False),
                budget=extracted_budget if extracted_budget != "None" else None,
                age=extracted_age if extracted_age != "None" else None,
                region=extracted_region if extracted_region != "None" else None
            )
            db.add(userinfo)

        db.commit()
        db.refresh(userinfo)

        return userinfo

def chat_statistics_add_or_update_data(json_data: dict, db: Session):
    
    statistics_id = json_data.get('id')
    chatroom_id = json_data.get('chatroom_id')

    with SessionLocal() as db:
        chatroom = db.query(ChatRoom).filter(ChatRoom.id == chatroom_id).first()

        if chatroom:
            ai = db.query(AI).filter(AI.id == chatroom.ai_id).first()

            if ai:
                existing_usage = json.loads(ai.usage) if ai.usage else {}
                ai_total_tokens = existing_usage.get('total_tokens', 0)

            else:
                ai_total_tokens = 0

        else:
            ai_total_tokens = 0
        
        # 기존 ChatStatistics를 조회합니다.
        statistics = db.query(ChatStatistics).filter(ChatStatistics.id == statistics_id).first()

        if statistics:
            statistics.chatroom_id = chatroom_id

            # 기존 total_tokens에 AI의 total_tokens 값을 추가합니다.
            statistics.total_tokens = (statistics.total_tokens or 0) + ai_total_tokens
            db.commit()  # 먼저 total_tokens를 업데이트 후 commit합니다.

        # statistics가(id) 존재하지 않을 경우 새 statistics를 추가합니다.
        else:
            statistics = ChatStatistics(
                id=statistics_id,
                chatroom_id=chatroom_id,
                total_chat_duration=chatroom.conversation_duration if chatroom else None,
                total_tokens=ai_total_tokens
            )
            db.add(statistics)
            db.commit()  # total_tokens를 설정하고 바로 commit합니다.

        # 모든 ChatStatistics의 total_tokens를 합산한 후 평균을 계산합니다.
        all_statistics = db.query(ChatStatistics).all()
        total_tokens_sum = sum((stats.total_tokens or 0) for stats in all_statistics)
        total_duration_sum = sum(
            (stats.total_chat_duration.total_seconds() if stats.total_chat_duration else 0) 
            for stats in all_statistics
        )
        chatroom_count = len(all_statistics) or 1
        
        # 평균값들을 업데이트합니다.
        average_tokens = total_tokens_sum / chatroom_count
        average_chat_duration_seconds = total_duration_sum / chatroom_count
        average_chat_duration = timedelta(seconds=average_chat_duration_seconds)

        statistics.average_chat_duration = average_chat_duration
        statistics.average_tokens = average_tokens

        db.commit()
        db.refresh(statistics)

        return statistics

def update_end_time(json_data: dict, db: Session):
    chatroom_id = json_data.get('id')
    end_time_str = json_data.get('end_time')
    end_time = datetime.fromisoformat(end_time_str) if end_time_str else None

    with SessionLocal() as db:
        # id로 ChatRoom을 조회합니다.
        chatroom = db.query(ChatRoom).filter(ChatRoom.id == chatroom_id).first()
        
        if chatroom:
            chatroom.end_time = end_time
            chatroom.conversation_duration = end_time - chatroom.start_time if end_time else None
            db.commit()

            # ChatStatistics를 조회하고 업데이트합니다.
            statistics = db.query(ChatStatistics).filter(ChatStatistics.chatroom_id == chatroom_id).first()
            if statistics:
                if statistics.total_chat_duration:
                    if chatroom.conversation_duration:
                        statistics.total_chat_duration += chatroom.conversation_duration
                else:
                    if chatroom.conversation_duration:
                        statistics.total_chat_duration = chatroom.conversation_duration
                
                db.commit()

            db.refresh(chatroom)
            db.refresh(statistics)
        else:
            print("해당하는 id의 chatroom은 존재하지 않습니다.")


# read

def time_and_token_search(chatroom_id: int, db: Session):
    with SessionLocal() as session:

        # 현재 시간을 담을 변수입니다.
        current_time = datetime.now()

        # ChatRoom과 AI 테이블을 조인하여 total_tokens를 가져옵니다.
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

        # last_chat_time, 현재 시간, total_tokens를 반환합니다.
        return {
            "last_chat_time" : last_chat_time,
            "current_time": current_time,
            "total_tokens": total_tokens
        }