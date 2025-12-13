"""Logging configuration"""
import sys
import io
from pathlib import Path
from loguru import logger
from app.core.config import settings


def setup_logger():
    """Setup application logger"""
    logger.remove()

    try:
        log_path = Path(settings.LOG_FILE)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        logger.add(log_path, format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
                   level=settings.LOG_LEVEL, rotation="10 MB", retention="7 days", compression="zip", encoding="utf-8", catch=True)
    except Exception:
        pass

    try:
        if sys.stdout is not None:
            stream = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace', line_buffering=True) if hasattr(sys.stdout, 'buffer') else sys.stdout
            logger.add(stream, format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
                       level=settings.LOG_LEVEL, colorize=True, catch=True)
    except Exception:
        pass

    if not logger._core.handlers:
        try:
            fallback = Path("logs/fallback.log")
            fallback.parent.mkdir(parents=True, exist_ok=True)
            logger.add(fallback, format="{time} | {level} | {message}", level="INFO", encoding="utf-8", catch=True)
        except Exception:
            logger.add(lambda _: None, level=settings.LOG_LEVEL)

    return logger


app_logger = setup_logger()
