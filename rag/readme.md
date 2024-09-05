상수 설명

- FOLDER_PATH = "./docs" 문서 경로를 입력해주세요.

- SPARSE_ENCODER_PATH = "./sparse_encoder.pkl" => 인코딩한 파일의 경로를 선택해주세요.
(인코딩한 파일이 없다면 
    process = Preprocess(folder_path='파일경로', sparse_encoder_path='인코딩 파일 경로/파일명.pkl')
    process.run()
를 실행해 주세요.)

- RAG_NAME = "interior-rag" => pinecone index name을 설정해주세요. 
(RAG_NAME에 언더바는 사용할 수 없습니다.)

- EMBEDDER_TYPE = "upstage" => embedder type은 두 가지 입니다. (openai, upstage)
DIMENSION = 4096 => Embedding 차원과 맞춥니다. 기본 설정은 upstage로 되어있습니다. (OpenAIEmbeddings: 1536, UpstageEmbeddings: 4096)

- METRIC = "dotproduct" => 유사도 측정 방법을 지정합니다. (dotproduct, euclidean, cosine) 
(HybridSearch 를 고려하고 있다면 metric 은 dotproduct 로 지정해야 합니다.)

- BATCH_SIZE = 32

사용법
- main.py의 question에 질문 내용을 넣으면 답변과 로그 기록을 확인 할 수 있습니다.

피드백
- 추가 예정

추후 업데이트
- 추가 예정

참고 자료
- 한글 전처리 & langchain (https://wikidocs.net/252407)