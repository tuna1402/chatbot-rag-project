import pprint


def create_kakao_response(gpt_message):
    kakao_response = {
        "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                            "text": gpt_message
                        }
                    }
                ]
            }
        }
    
    return kakao_response
    



# def add_history(talk_history, role, message):
#     pprint(talk_history)
#     history = talk_history.copy()
#     history.append({"role": role, "content": message})
#     return history