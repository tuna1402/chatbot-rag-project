# from PyPDF2 import PdfReader

# # pdf 파일 불러오기
# reader = PdfReader("./docs/interior_1.pdf")
# number_of_pages = len(reader.pages)
# page = reader.pages[0]
# text = page.extract_text()
# documents = reader.load()
# import time
# from langchain_community.document_loaders import PyPDFLoader
# loader = PyPDFLoader("./docs/interior_5.pdf")
# documents = loader.load()
# print(documents) # metadata
# print(type(documents)) # list
# print(len(page)) # 7 pages

# for i in range(len(documents)):
#     documents[i].page_content = documents[i].page_content.replace(u'\xa0', u'')
#     documents[i].page_content = documents[i].page_content.replace(u'\n', u'')

#텍스트 split
# from langchain_text_splitters import RecursiveCharacterTextSplitter

# text_splitter = RecursiveCharacterTextSplitter(
#     chunk_size = 1000,
#     chunk_overlap  = 100
# )

# texts = text_splitter.split_documents(documents)

# print(texts) # str

#embedding
# from langchain_openai import OpenAIEmbeddings

# embeddings_model = OpenAIEmbeddings()
# embeddings = [embeddings_model.embed_query(doc.page_content) for doc in texts]
# print(len(embeddings), len(embeddings[0]))

# # # embeddings 시각화 코드
# import matplotlib.pyplot as plt
# from sklearn.manifold import TSNE
# import numpy as np

# # # t-SNE를 사용하여 2차원으로 축소
# embeddings_array = np.array(embeddings)
# perplexity_value = min(5, len(embeddings_array)) #embedding된 len 수 보다 높아야 한다.
# tsne = TSNE(n_components=2, perplexity=perplexity_value, random_state=42)
# embeddings_2d = tsne.fit_transform(embeddings_array)

# # # 2차원으로 축소된 데이터를 시각화

# plt.figure(figsize=(10, 8))
# plt.scatter(embeddings_2d[:, 0], embeddings_2d[:, 1], c='blue', marker='o')
# plt.title('2D Visualization of Embeddings')
# plt.xlabel('TSNE Component 1')
# plt.ylabel('TSNE Component 2')
# plt.savefig('embedding_graph.png')

# chroma - vector db 저장
# from langchain_community.vectorstores import Chroma

# db = Chroma.from_texts(
#     texts, 
#     embeddings_model,
#     collection_name = 'history', # db 이름
#     persist_directory = './db/chromadb', # db 저장 공간
#     collection_metadata = {'hnsw:space': 'cosine'}, # 유사도 계산(코사인 유사도)
# )
# FAISS - vector db 저장
# from langchain_community.vectorstores import FAISS
# vectorstore = FAISS.from_documents(documents=texts, embedding=embeddings_model)

# prompt template
# from langchain_core.prompts import PromptTemplate

# prompt = PromptTemplate.from_template(
#     """You are an assistant for question-answering tasks. 
# Use the following pieces of retrieved context to answer the question. 
# If you don't know the answer, just say that you don't know. 
# Answer in Korean.
# And please follow the structure below to answer the question:

# #Question: 
# {question} 
# #Context: 
# {context} 

# #Answer:"""
# )

# chat prompt template
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema import SystemMessage, HumanMessage, AIMessage



# 유사도 기반 검색 테스트
# query = '무엇에 대한 문서인가요?'
# docs = db.similarity_search(query)
# print(docs[0].page_content)

# Retrival
# query = '반셀프 인테리어란?'
# retriever = db.as_retriever(search_kwargs={'k': 1})
# retriever = vectorstore.as_retriever()
# docs = retriever.invoke(query)
# print(docs[0])

# GPT 연동 테스트
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# llm = ChatOpenAI(model="gpt-4o-mini", temperature=1, max_tokens=150)
# output_parser = StrOutputParser()

# llm_answer = llm.invoke("반셀프 인테리어란?")
# print(llm_answer)
# chain = prompt | llm | retriever
# rag_answer = chain.invoke({"user_input": "전기 공사 비용은?"}).content
# print(rag_answer)

from langchain.chains import create_retrieval_chain, create_history_aware_retriever
from langchain_core.prompts import MessagesPlaceholder

# prompt_chain = (
#     {"context": retriever, "question": RunnablePassthrough()}
#     | prompt
#     | llm
#     | StrOutputParser()
# )

# chat_prompt = ChatPromptTemplate.from_messages([
#     MessagesPlaceholder(variable_name='chat_history'),
#     ("user", "{input}"),
#     ("user", "Given the above conversation, \
#      generate a search query to look up \
#      in order to get information relevant to the conversation. \
#      You are an assistant for question-answering tasks about the interior. \
#      Use the following pieces of retrieved context to answer the question. \
#      If you don't know the answer, just say that you don't know.")
# ])
# retriever_chain = create_history_aware_retriever(llm, retriever, chat_prompt)

# question1 = "전기 공사 인건비 얼마야?"
# chat_history = []

# ai_answer = retriever_chain.invoke({"input": question1, "chat_history": chat_history})

# print(ai_answer[0].page_content)

# chat_history.extend([
#     HumanMessage(content=question1),
#     AIMessage(content=ai_answer[0].page_content),
# ])

def rag_response(question: str, retriever_chain):
    chat_history = []
    ai_answer = retriever_chain.invoke({"input": question, "chat_history": chat_history})

    chat_history.extend([
        HumanMessage(content=question),
        AIMessage(content=ai_answer[0].page_content),
    ])
    
    return ai_answer[0].page_content