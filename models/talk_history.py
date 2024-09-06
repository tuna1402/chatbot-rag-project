class ChatRoom:
    def __init__(self, chatroom_id, ai_id, chatbot_id, user_id, userinfo_id):
        self.chatroom_id = chatroom_id
        self.ai_id = ai_id
        self.chatbot_id = chatbot_id
        self.user_id = user_id
        self.user_info = userinfo_id
        self.chat_history = []  # 배열을 이용한 채팅 기록 저장소
        #self.chatbot_name = chatbot_name
    

    # def get_chatbot_name(self):
    #     return self.chatbot_name
        
    def get_chatroom_id(self):
        return self.chatroom_id
    
    def get_ai_id(self):
        return self.ai_id
    
    def get_chatbot_id(self):
        return self.chatbot_id
    
    def get_user_id(self):
        return self.user_id
    
    def get_userinfo_id(self):
        return  self.user_info
    
    def add_message(self, message):
        """배열(채팅 기록)을 갱신하는 함수. 새 메시지를 추가함."""
        self.chat_history.append(message)
        print(f"새 메시지가 추가되었습니다: {message}")
    
    def get_chat_history(self):
        """현재까지의 채팅 기록을 반환하는 함수."""
        
        
            
        
        return self.chat_history

    def clear_chat_history(self):
        """채팅 기록을 초기화하는 함수."""
        self.chat_history = []
        print("채팅 기록이 초기화되었습니다.")
    
    def __str__(self):
        """클래스의 속성을 문자열로 반환하는 함수."""
        return (f"ChatRoom(chatroom_id={self.chatroom_id}, ai_id={self.ai_id}, "
                f"chatbo_it={self.chatbot_id}, user_id={self.user_id}, "
                f"chat_history={self.chat_history})")


# 사용 예시
# chat_room = ChatRoom(chatroom_id=1, ai_id=100, chatbot_id='ChatBot_X', user_id=500)

# chat_room.add_message("안녕하세요!")
# chat_room.add_message("무엇을 도와드릴까요?")
# print(chat_room.get_chat_history())

# chat_room.clear_chat_history()
# print(chat_room.get_chat_history())
