## essential API KEYs
- OPENAI_API_KEY(GPT 응답 받는 용도)
- PINECONE_API_KEY(임베딩한 데이터 저장용 DB)
- UPSTAGE_API_KEY(임베딩 타입)
- LANGCHAIN_API_KEY(RAG 라이브러리)

## constant descriptions
- FOLDER_PATH = "./docs" 문서 경로를 입력해주세요.

- SPARSE_ENCODER_PATH = "./sparse_encoder.pkl" => 인코딩한 파일의 경로를 선택해주세요.
(인코딩한 파일이 없다면 
    process = Preprocess(folder_path='파일경로', sparse_encoder_path='인코딩 파일 경로/파일명.pkl')
    process.run()
를 실행해 주세요.)

- RAG_NAME = "interior-rag" => pinecone index name을 설정해주세요. 
(RAG_NAME에 언더바는 사용할 수 없습니다.)

- EMBEDDER_TYPE = "upstage" => embedder type은 두 가지 입니다. (openai, upstage)
DIMENSION = 4096 => Embedding 차원과 맞춥니다. 기본 설정은 upstage로 되어있습니다. 
(OpenAIEmbeddings: 1536, UpstageEmbeddings: 4096)

- METRIC = "dotproduct" => 유사도 측정 방법을 지정합니다. (dotproduct, euclidean, cosine) 
(HybridSearch 를 고려하고 있다면 metric 은 dotproduct 로 지정해야 합니다.)

- BATCH_SIZE = 32

## How to use
- 필수 API를 모두 등록하십시오.
- main.py의 user_id와 question에 질문 내용을 넣으면 문서 임베딩, DB 저장 및 답변과 로그 확인이 한 번에 가능합니다.

    ### advanced usage
    - RAGSession의 파라미터를 수정하여 활용하십시오.
        (default: 
        model="gpt-4o-mini", temparature=0.25, max_tokens=750, 
        index_name='interior-rag', namespace='interior-rag', encoder_path="./sparse_encoder.pkl", top_k=5, alpha=0.75)

## feedbacks
- 추가 예정

## futher updates
- 추가 예정

### references
- 한글 전처리 & langchain (https://wikidocs.net/252407)