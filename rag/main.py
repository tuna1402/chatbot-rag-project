import os

#from preprocess import Preprocess
from rag.preprocess import Preprocess
from rag.upsert import Upsert
from rag.rag_session import RAGSession

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

def create_rag_session():
    
    return RAGSession()

def main(rag_obj: RAGSession, question: str):
    contents, metadatas = preprocess_documents()

    if contents and metadatas:
        upsert_documents(contents, metadatas)

    res = rag_obj.ask_question(question)
    his = rag_obj.chat_history

    return res, his

# if __name__ == "__main__":

#     user_id = 'abc'
#     utterance = "15평 피아노 학원 인테리어 견적 뽑아줘"

#     user_id = create_rag_session()
#     res = user_id.ask_question(utterance)
#     his = user_id.chat_history
    # print(res, his)
    # print(user_id.ask_question("10평으로 변경해서 알려줘"))
    # print(his)