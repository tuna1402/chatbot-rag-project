from generate import pinecone_retriever
from langchain_openai import ChatOpenAI
from lang_ch import rag_response
from langchain.chains import create_history_aware_retriever
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
import time

def get_rag_response(question: str) -> str:
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=1, max_tokens=300)
    retriever = pinecone_retriever
    chat_prompt = ChatPromptTemplate.from_messages([
        MessagesPlaceholder(variable_name='chat_history'),
        ("user", "{input}"),
        ("user", "Given the above conversation, generate a search query to look up in order to \
         get information relevant to the conversation. You are an assistant for question-answering tasks about the interior. \
         Use the following pieces of retrieved context to answer the question. \
         If you don't know the answer, just say that you don't know.")
    ])

    retriever_chain = create_history_aware_retriever(llm, retriever, chat_prompt)

    start_time = time.time()

    # 질문을 받아 응답 생성
    res = rag_response(question, retriever_chain)
    
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Execution Time: {execution_time} seconds")

    return res

if __name__ == "__main__":
    
    question1 = "가게 인테리어 할 때 필요한 정보는 무엇이 있습니까?"
    response = get_rag_response(question1)
    print(response)