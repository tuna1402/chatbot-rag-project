import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore_v1 import Client

# Firebase 서비스 계정 키 파일 경로 설정
cred = credentials.Certificate("path/to/your/firebase-adminsdk.json")

# Firebase Admin SDK를 초기화하여 Firestore 데이터베이스에 접근할 수 있도록 설정합니다.
firebase_admin.initialize_app(cred)

# Firestore 데이터베이스 객체를 생성합니다.
db: Client = firestore.client()

# Firestore에 유저가 보낸 메시지와 GPT 응답을 저장하는 함수입니다.
def save_chat_and_response_to_firestore(user_id, user_message, gpt_response, chat_token_usage, response_token_usage):
    # 특정 유저의 메시지를 저장하기 위한 참조를 설정합니다.
    # 'kakao_chatbot' 컬렉션에 각 유저의 ID를 기준으로 Document를 생성하고, 그 안에 'messages'라는 서브컬렉션을 만듭니다.
    messages_ref = db.collection('kakao_chatbot').document(user_id).collection('messages')
    
    # Firestore에 메시지 데이터를 추가합니다.
    try:
        messages_ref.add({
            'userMessage': user_message,  # 유저가 보낸 메시지를 저장합니다.
            'gptResponse': gpt_response,  # GPT가 생성한 응답을 저장합니다.
            'chatTokenUsage': chat_token_usage,  # 해당 대화에서 사용된 토큰 수를 저장합니다.
            'responseTokenUsage': response_token_usage,  # GPT 응답에서 사용된 토큰 수를 저장합니다.
            'timestamp': firestore.SERVER_TIMESTAMP  # 서버 시간을 타임스탬프로 저장하여 기록된 시간을 표시합니다.
        })
        print(f"Saved chat and response for user {user_id}")  # 성공적으로 저장된 경우 콘솔에 메시지를 출력합니다.
    except Exception as e:
        print(f"Error saving chat and response: {e}")  # 데이터 저장 중 오류가 발생했을 때 오류 메시지를 콘솔에 출력합니다.

# Firestore에서 특정 유저의 모든 메시지와 GPT 응답 데이터를 가져오는 함수입니다.
def get_messages_and_responses_from_firestore(user_id):
    # 특정 유저의 메시지를 가져오기 위한 참조를 설정합니다.
    # 'kakao_chatbot' 컬렉션에 있는 해당 유저의 ID Document에서 'messages' 서브컬렉션을 가져옵니다.
    messages_ref = db.collection('kakao_chatbot').document(user_id).collection('messages')
    
    # 메시지를 타임스탬프 순서대로 정렬하여 가져옵니다.
    try:
        docs = messages_ref.order_by('timestamp').stream()  # Firestore에서 데이터를 가져옵니다.
        messages = []  # 가져온 메시지 데이터를 저장할 리스트를 초기화합니다.
        for doc in docs:  # 각 Document(메시지)마다 순회하면서 데이터를 리스트에 추가합니다.
            messages.append({
                'id': doc.id,  # 메시지 문서의 고유 ID를 저장합니다.
                'userMessage': doc.to_dict().get('userMessage'),  # 유저가 보낸 메시지를 리스트에 추가합니다.
                'gptResponse': doc.to_dict().get('gptResponse'),  # GPT가 생성한 응답을 리스트에 추가합니다.
                'chatTokenUsage': doc.to_dict().get('chatTokenUsage'),  # 채팅에 사용된 토큰 수를 리스트에 추가합니다.
                'responseTokenUsage': doc.to_dict().get('responseTokenUsage'),  # GPT 응답에서 사용된 토큰 수를 리스트에 추가합니다.
                'timestamp': doc.to_dict().get('timestamp')  # 해당 메시지의 타임스탬프를 리스트에 추가합니다.
            })
        return messages  # 수집한 메시지 데이터를 반환합니다.
    except Exception as e:
        print(f"Error fetching messages and responses: {e}")  # 데이터를 가져오는 중에 오류가 발생했을 때 오류 메시지를 콘솔에 출력합니다.
        return None

# 함수 테스트를 위해 메인 루틴을 작성할 수도 있습니다.
if __name__ == "__main__":
    # Firestore에 메시지와 GPT 응답을 저장하는 예제
    save_chat_and_response_to_firestore("user1", "Hello", "Hi there!", 5, 7)

    # Firestore에서 메시지와 응답 데이터를 가져오는 예제
    messages = get_messages_and_responses_from_firestore("user1")
    print(messages)
