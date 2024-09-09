from all_def import create_pinecone_retriever
from langchain_openai import ChatOpenAI
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.schema import HumanMessage, AIMessage


class RAGSession:
    def __init__(self, model="gpt-4o-mini", temparature=0.25, max_tokens=750, 
                 index_name='interior-rag', namespace='interior-rag', encoder_path="./sparse_encoder.pkl", top_k=5, alpha=0.75):
        
        self.chat_history = []
        self.llm = ChatOpenAI(model=model, temperature=temparature, max_tokens=max_tokens)
        self.retriever = create_pinecone_retriever(
            
            index_name=index_name,
            namespace=namespace,
            encoder_path=encoder_path,
            top_k=top_k,
            alpha=alpha

        )

        system_prompt = (
            "You are an assistant helping with interior queries. "
            "but if the context does not contain the answer, "
            "use your own knowledge to answer the question."
            "use friendly way to talk"
            "\n\n"
            "{context}"
        )

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
                                    self.llm, self.retriever, contextualize_q_prompt
                                    )
        
        qa_prompt = ChatPromptTemplate.from_messages(
                    [
                        ("system", system_prompt),
                        MessagesPlaceholder("chat_history"),
                        ("human", "{input}"),
                    ]
                )

        question_answer_chain = create_stuff_documents_chain(self.llm, qa_prompt)
        self.rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)

    def ask_question(self, question):
        ai_msg = self.rag_chain.invoke({"input": question, "chat_history": self.chat_history})
        self.chat_history.extend([
                            HumanMessage(content=question),
                            AIMessage(content=ai_msg["answer"]),
                        ])
        
        return ai_msg["answer"]


if __name__ == "__main__":

    user_session1 = RAGSession()
    user_session2 = RAGSession()
    response1 = user_session1.ask_question("What is the best color for a small living room?")
    response2 = user_session2.ask_question("15평 바닥 공사 비용 얼마야?")
    response2 = user_session2.ask_question("요즘 유행하는 상가 인테리어 디자인 알려줘")
    print(response1)
    print(response2)
    print(user_session1.chat_history)
    print(user_session2.chat_history)
