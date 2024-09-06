from rag.all_def import create_pinecone_retriever
import os

pinecone_api_key = os.getenv("PINECONE_API_KEY")

pinecone_retriever = create_pinecone_retriever(
    index_name="interior-rag",
    namespace="interior-rag",
    encoder_path="./sparse_encoder.pkl",
    top_k=1,
    alpha=0.75
)

# search_results = pinecone_retriever.invoke("전기 공사 인건비 얼마야?")
# for result in search_results:
#     print(result.page_content)
#     print('\n')
#     print(result.metadata)