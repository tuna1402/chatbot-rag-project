from all_def import pdf_reader_and_split, divide_metacon, corpus_gen, token_split
import os

openai_api_key = os.getenv("OPENAI_API_KEY")
upstage_api_key = os.getenv("UPSTAGE_API_KEY")

folder_path = './docs' # encoding할 데이터 경로
split_texts = pdf_reader_and_split(folder_path, token_split)

contents, metadatas = divide_metacon(split_texts)
sparse_encoder_path = "./sparse_encoder.pkl" # 파일명 설정
corpus_gen(sparse_encoder_path, contents) # 파일 생성, 같은 이름 예외처리