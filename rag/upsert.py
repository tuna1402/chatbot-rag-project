from all_def import create_index, load_sparse_encoder, upsert_doc
from preprocess import contents, metadatas
from langchain_openai import OpenAIEmbeddings
from langchain_upstage import UpstageEmbeddings
import os

pinecone_api_key = os.getenv("PINECONE_API_KEY")

#api_key:str, name:str = 'interior-rag', dimension:int = 4096, metric:str = 'cosine'
pc_index = create_index(pinecone_api_key, 'interior-rag', 4096, 'dotproduct')

# 둘 중 용도에 맞는 embedding 선택
# openai_embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
upstage_embeddings = UpstageEmbeddings(model="solar-embedding-1-large-passage")
sparse_encoder = load_sparse_encoder("./sparse_encoder.pkl")


upsert_doc(pc_index, 'interior-rag', contents, metadatas, sparse_encoder, 
               embedder=upstage_embeddings, batch_size=32)