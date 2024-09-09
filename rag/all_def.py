'''

1. pdf 데이터 읽어오기
2. pdf 데이터 확인 - 메타 데이터 형식
3. text split
    3.1 - CharacterTextSplitter("\n\n" 기준)
    3.2 - RecursiveCharacterTextSplitter(문자 수 기반)
    3.3 - TokenTextSplitter(토큰 수 기반 chunk 생성)
    3.4 - SemanticChunker(의미론적 유사성 기반)
    3.5 - pdf & split 함수
4. 텍스트 전처리
5. pinecone index 생성
6. embedding upsert
7. retrival

'''


#======================================================================
# 1. DATA LOAD(pdf)

from langchain_community.document_loaders import PyPDFLoader
import os

def pdf_loader(file_path):
    
    try:
        loader = PyPDFLoader(file_path)
        documents = loader.load()
        return documents
    
    except Exception as e: # 못 읽는 pdf 파일 예외 처리
        print(f"Error pdf {file_path}: {e}")
        print(file_path.strip())
        return None

#======================================================================
# 2. DATA READ(pdf)

def pdf_reader(folder_path):
    
    all_documents = []

    for doc in os.listdir(folder_path):
        data = os.path.join(folder_path, doc)
        
        if data.endswith('.pdf'):
            documents = pdf_loader(data)
            if documents:
                all_documents.append(documents)
    
    return all_documents # 리스트 안에 담긴 메타 데이터 형태{source, page, page_content}

#test code
# all_documents = pdf_reader('./docs')
# print(len(all_documents)) # 14개 (3번-word 제외)
# print(all_documents[0]) # 문서 확인
# print(type(all_documents[0][0])) # base.Document

# 3. TEXT SPLIT

#======================================================================
# 3-1. character split
from langchain_text_splitters import CharacterTextSplitter

def char_split(doc):
    text_splitter = CharacterTextSplitter(
        # 텍스트를 분할할 때 사용할 구분자를 지정합니다. 기본값은 "\n\n"입니다.
        # separator=" ",
        # 분할된 텍스트 청크의 최대 크기를 지정합니다.
        chunk_size=250,
        # 분할된 텍스트 청크 간의 중복되는 문자 수를 지정합니다.
        chunk_overlap=50,
        # 텍스트의 길이를 계산하는 함수를 지정합니다.
        length_function=len,
        # 구분자가 정규식인지 여부를 지정합니다.
        is_separator_regex=False,
    )
    texts = text_splitter.split_documents(doc)
    return texts

#test code
# texts = char_split(all_documents[0])
# print(texts[1].page_content)

#======================================================================
# 3-2. recursive_split
from langchain_text_splitters import RecursiveCharacterTextSplitter

def recur_split(doc):
    text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 1000,
    chunk_overlap  = 100,
)
    texts = text_splitter.split_documents(doc)
    return texts

#======================================================================
# 3-3 token_split
def token_split(doc):
    text_splitter = CharacterTextSplitter.from_tiktoken_encoder(
        chunk_size = 1000,
        chunk_overlap = 0,
    )
    texts = text_splitter.split_documents(doc)
    return texts

#======================================================================
# 3-4 semantic chunker (pip install lanchain_experimental) - 미완성
from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai.embeddings import OpenAIEmbeddings

def sementic_chunk(doc):
    # OpenAI 임베딩을 사용하여 의미론적 청크 분할기를 초기화
    text_splitter = SemanticChunker(OpenAIEmbeddings())
    chunks = text_splitter.split_documents(doc)
    return chunks

#======================================================================
# 3-5. pdf read & split 한 번에 처리
from itertools import chain

def pdf_reader_and_split(folder_path, split_method):
    all_documents = pdf_reader(folder_path)
    
    # chain을 사용하여 모든 문서를 하나의 이터레이터로 연결
    flattened_docs = chain.from_iterable(all_documents)
    
    # 리스트 컴프리헨션을 사용하여 모든 문서를 한 번에 분할
    split_texts = [chunk for doc in flattened_docs for chunk in split_method([doc])]
    
    return split_texts

# test 코드
# split_texts = pdf_reader_and_split('./docs', token_split)
# print(type(split_texts)) # list[Document]
# print(split_texts[:5])

#======================================================================
# 4. text 전처리

# 모든 page_contents 데이터
# contents = [contents for split_text in split_texts 
#             for i, contents in enumerate(split_text[i].page_content)]
# print(contents[:10])
# print(split_texts[0].metadata) # source, page

#======================================================================
# 4.1 Documents object의 metadata와 page_content 구분
from langchain_teddynote.community.pinecone import preprocess_documents

def divide_metacon(split_texts):

    contents, metadatas = preprocess_documents(
        split_docs=split_texts,
        metadata_keys=["source", "page"],
        min_length=5,
        use_basename=True,
    )

    return contents, metadatas
    # test
    # print(contents[:5])
    # print(metadatas.keys())

#======================================================================
# 4.2 sparse encoder 생성
'''
tokenizer & 불용어 처리
sparse encoder(규제화 한 종류, dropout과 유사)를 사용해 텍스트 파일 학습
학습한 encoder는 vector store에 저장할 때 sparse vector를 생성하는 용도로 사용

'''
from langchain_teddynote.korean import stopwords
from langchain_teddynote.community.pinecone import (
    create_sparse_encoder,
    fit_sparse_encoder,
)

# sparse_encoder_path = "./sparse_encoder.pkl"

# # # 한글 불용어 사전 + Kiwi 형태소 분석기를 사용합니다.
def corpus_gen(sparse_encoder_path, contents):

    sparse_encoder = create_sparse_encoder(stopwords(), mode="kiwi")
    
    # # Sparse Encoder 를 사용하여 contents 를 학습
    if not os.path.exists(sparse_encoder_path):
        fit_sparse_encoder(
            sparse_encoder=sparse_encoder, 
            contents=contents, 
            save_path=sparse_encoder_path
        )

    else:
        print(f"'{sparse_encoder_path}' 파일이 이미 존재합니다.")

#======================================================================
# 5. embedding 저장용 serverless index 생성(pine cone) 
# pip install "pinecone-client[grpc]"

from pinecone import Pinecone, ServerlessSpec

pinecone_api_key = os.getenv("PINECONE_API_KEY")

def create_index(pinecone_api_key:str, 
                 name:str = 'interior-rag', 
                 dimension:int = 4096,
                 metric:str = 'dotproduct'):
# Pinecone 초기화
    pc = Pinecone(api_key=pinecone_api_key)

    pc.create_index(
    name=name,
    dimension=dimension, # open AI embedding: 1536, upstage embedding: 4096
    metric=metric,
    spec=ServerlessSpec(
        cloud="aws",
        region="us-east-1"
        ),
    deletion_protection="disabled"
    )

    pc_index = pc.Index("interior-rag")
    
    return pc_index

#======================================================================
# 6. db 인덱스에 upsert
from langchain_openai import OpenAIEmbeddings
from langchain_upstage import UpstageEmbeddings
from langchain_teddynote.community.pinecone import upsert_documents
from langchain_teddynote.community.pinecone import load_sparse_encoder

# openai_embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
# upstage_embeddings = UpstageEmbeddings(model="solar-embedding-1-large-passage")

# 추후에 학습된 sparse encoder 를 불러올 때 사용합니다.
# sparse_encoder = load_sparse_encoder("./sparse_encoder.pkl")

def upsert_doc(index, namespace, contents, metadatas, sparse_encoder, 
               embedder=UpstageEmbeddings, batch_size=32):

    upsert_documents(
        index=index,  # Pinecone 인덱스
        namespace=namespace,  # Pinecone namespace
        contents=contents,  # 이전에 전처리한 문서 내용
        metadatas=metadatas,  # 이전에 전처리한 문서 메타데이터
        sparse_encoder=sparse_encoder,  # Sparse encoder
        embedder=embedder,
        batch_size=batch_size,
    )

#======================================================================
# 7. retrieval

from langchain_teddynote.community.pinecone import init_pinecone_index
from langchain_teddynote.community.pinecone import PineconeKiwiHybridRetriever

def retriever_base():
    
    index_name = None
    namespace = None
    encoder_path = None

    pinecone_params = init_pinecone_index(
            index_name=index_name,  
            namespace=namespace,  
            api_key=pinecone_api_key,  
            sparse_encoder_path=encoder_path,  
            stopwords=stopwords(),  
            tokenizer="kiwi",
            embeddings=UpstageEmbeddings(
                model="solar-embedding-1-large-query"
            ),  # Dense Embedder
            top_k=5,  # Top-K 문서 반환 개수
            alpha=0.25,  # alpha=0.75로 설정한 경우, (0.75: Dense Embedding, 0.25: Sparse Embedding)
        )

    # 검색기 생성
    pinecone_retriever = PineconeKiwiHybridRetriever(**pinecone_params)
    
    return pinecone_retriever

from typing import Optional, List
from langchain_upstage  import UpstageEmbeddings

def create_pinecone_retriever(
    index_name: Optional[str] = None,
    namespace: Optional[str] = None,
    encoder_path: Optional[str] = None,
    pinecone_api_key: Optional[str] = None,
    stopwords: Optional[List[str]] = None,
    tokenizer: str = "kiwi",
    embedding_model: str = "solar-embedding-1-large-query",
    top_k: int = 5,
    alpha: float = 0.5
) -> PineconeKiwiHybridRetriever:

    if not index_name:
        raise ValueError("index 이름이 잘못되었습니다.")

    if not pinecone_api_key:
        pinecone_api_key = os.environ.get("PINECONE_API_KEY")
        if not pinecone_api_key:
            raise ValueError("api key를 설정하세요. PINECONE_API_KEY")

    if not stopwords:
        from langchain_teddynote.korean import stopwords
        stopwords = stopwords()

    pinecone_params = init_pinecone_index(
        index_name=index_name,
        namespace=namespace,
        api_key=pinecone_api_key,
        sparse_encoder_path=encoder_path,
        stopwords=stopwords,
        tokenizer=tokenizer,
        embeddings=UpstageEmbeddings(model=embedding_model),
        top_k=top_k,
        alpha=alpha,
    )

    pinecone_retriever = PineconeKiwiHybridRetriever(**pinecone_params)

    return pinecone_retriever

if __name__ == "__main__":

    pinecone_retriever = create_pinecone_retriever(
    index_name="interior-rag",
    namespace="interior-rag",
    encoder_path="./sparse_encoder.pkl",
    top_k=10,
    alpha=0.75
    )

    search_results = pinecone_retriever.invoke("전기 공사 인건비 얼마야?")
    for result in search_results:
        print(result.page_content)
        print('\n')
        print(result.metadata)