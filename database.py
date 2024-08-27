# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
from dotenv import load_dotenv

load_dotenv()  # .env 파일에서 환경 변수를 로드

DATABASE_URL = os.getenv("DATABASE_URL")

# SQLAlchemy를 사용하여 데이터베이스 엔진을 생성
engine = create_engine(DATABASE_URL, echo=False)

# 세션을 생성하기 위한 세션메이커 (sessionmaker)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# SQLAlchemy 모델의 베이스 클래스
Base = declarative_base()

# 의존성 주입을 위한 데이터베이스 세션 생성 함수
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
