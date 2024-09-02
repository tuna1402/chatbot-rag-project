from generate import pinecone_retriever
from langchain_openai import ChatOpenAI
from lang_ch import rag_response
from langchain.chains import create_history_aware_retriever
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
import time

llm = ChatOpenAI(model="gpt-4o-mini", temperature=1, max_tokens=300)
retriever = pinecone_retriever
chat_prompt = ChatPromptTemplate.from_messages([
    MessagesPlaceholder(variable_name='chat_history'),
    ("user", "{input}"),
    ("user", "Given the above conversation, \
     generate a search query to look up \
     in order to get information relevant to the conversation. \
     You are an assistant for question-answering tasks about the interior. \
     Use the following pieces of retrieved context to answer the question. \
     If you don't know the answer, just say that you don't know.")
])

retriever_chain = create_history_aware_retriever(llm, retriever, chat_prompt)

start_time = time.time()

question1 = "가게 인테리어 할 때 필요한 정보는 무엇이 있습니까?"

res = rag_response(question1, retriever_chain)
end_time = time.time()
print(res)
execution_time = end_time - start_time
print(execution_time)