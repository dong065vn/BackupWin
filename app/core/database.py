"""Database connection and session management"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings
from app.core.logger import app_logger

engine = SessionLocal = None

try:
    db_url = settings.DATABASE_URL.replace("postgresql://", "postgresql+psycopg://", 1) if settings.DATABASE_URL.startswith("postgresql://") else settings.DATABASE_URL
    engine = create_engine(db_url, pool_pre_ping=True, echo=False)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    app_logger.info("Database engine created")
except Exception as e:
    app_logger.warning(f"Database not available: {e}")

Base = declarative_base()


def get_db():
    if SessionLocal is None:
        yield None
        return
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    if engine is None:
        app_logger.warning("Database not available")
        return
    try:
        Base.metadata.create_all(bind=engine)
        app_logger.info("Database tables created")
    except Exception as e:
        app_logger.error(f"Error creating tables: {e}")
        raise
