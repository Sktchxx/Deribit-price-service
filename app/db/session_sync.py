from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import DATABASE_SYNC_URL


engine = create_engine(DATABASE_SYNC_URL)
SessionLocal = sessionmaker(bind=engine)
