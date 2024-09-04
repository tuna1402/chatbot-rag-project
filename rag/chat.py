from generate import pinecone_retriever
from langchain_openai import ChatOpenAI
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.schema import HumanMessage, AIMessage

chat_history = []

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.5, max_tokens=750)
retriever = pinecone_retriever

system_prompt = (
"You are an assistant helping with interior queries. \
but if the context does not contain the answer, \
use your own knowledge to answer the question."
"\n\n"
"{context}"
)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}")
    ]
)

question_answer_chain = create_stuff_documents_chain(llm, prompt)
rag_chain = create_retrieval_chain(retriever, question_answer_chain)

contextualize_q_system_prompt = (
    "Given a chat history and the latest user question "
    "which might reference context in the chat history, "
    "formulate a standalone question which can be understood "
    "without the chat history. Do NOT answer the question, "
    "just reformulate it if needed and otherwise return it as is."
    )

contextualize_q_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", contextualize_q_system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
    )

history_aware_retriever = create_history_aware_retriever(
        llm, retriever, contextualize_q_prompt
    )

qa_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
    )

question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)
rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)

def rag_qa(question):
    ai_msg = rag_chain.invoke({"input": question, "chat_history": chat_history})
    chat_history.extend([
        HumanMessage(content=question),
        AIMessage(content=ai_msg["answer"]),
    ])

    return ai_msg["answer"]

if __name__ == "__main__":

    question1 = "18평 인테리어 공사 평균 비용 알려줘"
    question2 = "그 중에서 전기 공사 비용은 얼마나 되?"
    a1 = rag_qa(question1)
    a2 = rag_qa(question2)
    print(a1, a2)
    print(chat_history)