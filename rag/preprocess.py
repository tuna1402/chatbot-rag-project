from all_def import pdf_reader_and_split, divide_metacon, corpus_gen, token_split
import os

# openai_api_key = os.getenv("OPENAI_API_KEY")
# upstage_api_key = os.getenv("UPSTAGE_API_KEY")

# folder_path = './docs' # encoding할 데이터 경로
# split_texts = pdf_reader_and_split(folder_path, token_split)

# contents, metadatas = divide_metacon(split_texts)
# sparse_encoder_path = "./sparse_encoder.pkl" # 파일명 설정
# corpus_gen(sparse_encoder_path, contents) # 파일 생성, 같은 이름 예외처리

class Preprocess():

    openai_api_key = os.getenv("OPENAI_API_KEY")
    upstage_api_key = os.getenv("UPSTAGE_API_KEY")

    def __init__(self, folder_path='./docs', sparse_encoder_path='./sparse_encoder.pkl'):

        self.folder_path = folder_path
        self.sparse_encoder_path = sparse_encoder_path
        self.split_texts = None
        self.contents = None
        self.metadatas = None

    def create_split_texts(self, token_split):
        self.split_texts = pdf_reader_and_split(self.folder_path, token_split)
        print(self.split_texts[:3])
        return self.split_texts
    
    def create_meta_content(self):
        self.contents, self.metadatas = divide_metacon(self.split_texts)
        return self.contents, self.metadatas
    
    def corpus_gen(self):
        corpus_gen(self.sparse_encoder_path, self.contents)

    def run(self):
        self.create_split_texts(token_split)
        print("split text finished")
        self.create_meta_content()
        print("metadata, contents finished")
        self.corpus_gen()
        print("corpus finished")

if __name__ == "__main__":

    folder_path = './docs'
    sparse_encoder_path = './pkl_name.pkl'

    process = Preprocess(folder_path=folder_path, sparse_encoder_path=sparse_encoder_path)
    process.run()