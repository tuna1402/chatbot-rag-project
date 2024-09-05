import os

from preprocess import Preprocess
from upsert import Upsert
from rag_session import RAGSession

FOLDER_PATH = "./docs"
SPARSE_ENCODER_PATH = "./sparse_encoder.pkl"
RAG_NAME = "interior-rag"
DIMENSION = 4096
METRIC = "dotproduct"
EMBEDDER_TYPE = "upstage"
BATCH_SIZE = 32

def preprocess_documents():

    if not os.path.exists(SPARSE_ENCODER_PATH):

        process = Preprocess(folder_path=FOLDER_PATH, sparse_encoder_path=SPARSE_ENCODER_PATH)
        process.run()
        return process.contents, process.metadatas

    else:
        print(f"전처리 과정을 건너 뜁니다. {SPARSE_ENCODER_PATH}가 이미 존재합니다.")
        return None, None

def upsert_documents(contents, metadatas):

    try:
        upsert = Upsert(rag_name=RAG_NAME, dimension=DIMENSION, metric=METRIC, file_path=SPARSE_ENCODER_PATH)
        upsert.run(contents, metadatas, EMBEDDER_TYPE, BATCH_SIZE)

    except Exception as e:
        print(f"에러가 발생했습니다. 에러 내용: {e}. 임베딩 업로드를 건너 뜁니다.")

def main(user_id:str, question):

    contents, metadatas = preprocess_documents()

    if contents and metadatas:
        upsert_documents(contents, metadatas)

    user_id = RAGSession()
    response = user_id.ask_question(question)
    hisory = user_id.chat_history

    return  response, hisory 

if __name__ == "__main__":

    user_id = 'abc'
    utterance = "15평 피아노 학원 인테리어 견적 뽑아줘"

    res, his = main(user_id, utterance)
    print(res)
    