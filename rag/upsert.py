from all_def import create_index, load_sparse_encoder, upsert_doc
from preprocess import Preprocess
from langchain_openai import OpenAIEmbeddings
from langchain_upstage import UpstageEmbeddings
import os

# pinecone_api_key = os.getenv("PINECONE_API_KEY")

# #api_key:str, name:str = 'interior-rag', dimension:int = 4096, metric:str = 'cosine'
# pc_index = create_index(pinecone_api_key, 'interior-rag', 4096, 'dotproduct')

# # 둘 중 용도에 맞는 embedding 선택
# openai_embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
# upstage_embeddings = UpstageEmbeddings(model="solar-embedding-1-large-passage")
# sparse_encoder = load_sparse_encoder("./sparse_encoder.pkl")


# upsert_doc(pc_index, 'interior-rag', contents, metadatas, sparse_encoder, 
#                embedder=upstage_embeddings, batch_size=32)

class Upsert():

    pinecone_api_key = os.getenv("PINECONE_API_KEY")

    def __init__(self, rag_name, dimension, metric, file_path):

        self.rag_name = rag_name
        self.dimension = dimension
        self.metric = metric
        self.file_path = file_path
        self.pc_index = self.pinecone_index_create()

    def pinecone_index_create(self):

        return create_index(self.pinecone_api_key, self.rag_name, self.dimension, self.metric)
    
    def load_embeddings(self, embedder_type: str):

        if embedder_type == 'openai':
            return OpenAIEmbeddings(model="text-embedding-3-large")
        elif embedder_type == 'upstage':
            return UpstageEmbeddings(model="solar-embedding-1-large-passage")
        else:
            raise ValueError(f"embedding 타입을 잘못 입력했습니다.: {embedder_type}")

    def sparse_data_load(self):

        self.sparse_encoder = load_sparse_encoder(self.file_path)
        return self.sparse_encoder
    
    def upsert_file(self, contents, metadatas, embedder_type: str, batch_size: int):
        embedder = self.load_embeddings(embedder_type)
        self.sparse_encoder = self.sparse_data_load()
        upsert_doc(self.pc_index, self.rag_name, contents, metadatas, self.sparse_encoder, 
               embedder, batch_size)
        
    def run(self, contents, metadatas, embedder_type:str, batch_size:int):
        self.upsert_file(contents, metadatas, embedder_type, batch_size)

if __name__ == "__main__":
    
    upsert = Upsert(rag_name="interior-rag", dimension=4096, metric="dotproduct", file_path="./sparse_encoder.pkl")
    preprocess = Preprocess()
    upsert.run(preprocess.contents, preprocess.metadatas, "upstage", 32)