from preprocess import Preprocess
from upsert import Upsert

folder_path = "./docs"
sparse_encoder_path = "C:\\Users\\SAMSUNG\\Desktop\\kakao_team\\dev2_240902\\chatbot-rag-project\\sparse_encoder.pkl"

process = Preprocess(folder_path, sparse_encoder_path)
process.run()

upsert = Upsert("interior-rag", 4096, "dotproduct", sparse_encoder_path)
upsert.run(process.contents, process.metadatas, "upstage", 32)