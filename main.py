"""Main application entry point"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router
from app.core.config import settings
from app.core.logger import app_logger
from app.core.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    app_logger.info("Starting BackupWin API...")
    try:
        init_db()
        app_logger.info("Database initialized")
    except Exception as e:
        app_logger.error(f"Startup error: {e}")
        raise
    yield
    app_logger.info("Shutting down...")


app = FastAPI(title=settings.API_TITLE, version=settings.API_VERSION, description="BackupWin - Windows File Backup and Search API",
              docs_url="/docs", redoc_url="/redoc", lifespan=lifespan)

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.include_router(router, prefix="/api/v1")


@app.get("/")
async def root():
    return {"message": "Welcome to BackupWin API", "version": settings.API_VERSION, "docs": "/docs", "health": "/api/v1/health"}


if __name__ == "__main__":
    import uvicorn
    app_logger.info(f"Starting server on {settings.API_HOST}:{settings.API_PORT}")
    uvicorn.run("main:app", host=settings.API_HOST, port=settings.API_PORT, reload=True, log_config=None)
