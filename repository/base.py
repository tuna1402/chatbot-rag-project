from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# DATABASE_URL = 데이터베이스 URL
# engine = 엔진 생성
# SessionLocal = 세션 생성
# Base = 기본 클래스 생성

DATABASE_URL = "postgresql://postgres:1234@localhost/chatbot"
engine = create_engine(DATABASE_URL, echo=True)  # echo=True로 SQL 로그 활성화
SessionLocal = sessionmaker(autocommit=False, autoflush=True, bind=engine)
Base = declarative_base()
