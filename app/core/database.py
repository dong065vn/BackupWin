"""Database connection and session management"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings
from app.core.logger import app_logger

# Create database engine
engine = None
SessionLocal = None

try:
    # Convert postgresql:// to postgresql+psycopg:// for psycopg3 support
    db_url = settings.DATABASE_URL
    if db_url.startswith("postgresql://"):
        db_url = db_url.replace("postgresql://", "postgresql+psycopg://", 1)

    engine = create_engine(
        db_url,
        pool_pre_ping=True,
        echo=False
    )
    # Create SessionLocal class
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    app_logger.info("Database engine created successfully")
except Exception as e:
    app_logger.warning(f"Database not available (GUI can still run): {e}")
    # GUI can still run without database
    engine = None
    SessionLocal = None

# Create Base class for models
Base = declarative_base()


def get_db():
    """
    Dependency for getting database session

    Yields:
        Database session
    """
    if SessionLocal is None:
        app_logger.warning("Database not available, skipping session creation")
        yield None
        return

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize database tables"""
    if engine is None:
        app_logger.warning("Database not available, skipping table creation")
        return

    try:
        Base.metadata.create_all(bind=engine)
        app_logger.info("Database tables created successfully")
    except Exception as e:
        app_logger.error(f"Error creating database tables: {e}")
        raise
