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

def main(question):

    if not os.path.exists(SPARSE_ENCODER_PATH):

        process = Preprocess(folder_path=FOLDER_PATH, sparse_encoder_path=SPARSE_ENCODER_PATH)
        process.run()
        contents, metadatas = process.contents, process.metadatas
    else:
        print(f"전처리 과정을 건너 뜁니다. {SPARSE_ENCODER_PATH}가 이미 존재합니다.")
        contents, metadatas = None, None

    try:
        upsert = Upsert(rag_name=RAG_NAME, dimension=DIMENSION, metric=METRIC, file_path=SPARSE_ENCODER_PATH)
        upsert.run(contents, metadatas, EMBEDDER_TYPE, BATCH_SIZE)

    except Exception as e:
        print(f"에러가 발생했습니다. 에러 내용: {e}. 임베딩 업로드를 건너 뜁니다.")

    user_session = RAGSession()
    response = user_session.ask_question(question)

    print(response)
    print(user_session.chat_history)

    return response, user_session.chat_history

if __name__ == "__main__":
    question = "15평 아파트 인테리어 평균 비용"
    main(question)