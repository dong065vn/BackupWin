"""Logging configuration"""
import sys
from pathlib import Path
from loguru import logger
from app.core.config import settings


def setup_logger():
    """Setup application logger with file and console output"""

    # Remove default logger
    logger.remove()

    try:
        # Try to set up file logger first
        log_path = Path(settings.LOG_FILE)
        # Create logs directory if it doesn't exist
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        logger.add(
            log_path,
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
            level=settings.LOG_LEVEL,
            rotation="10 MB",
            retention="7 days",
            compression="zip",
            encoding="utf-8",  # Use UTF-8 encoding for file output
            catch=True  # Prevent logger from crashing the app
        )
    except Exception as e:
        # If we can't create log file, continue with console only
        pass

    try:
        # Try to add console logger if stdout is available
        if sys.stdout is not None:
            # On Windows, wrap stdout with UTF-8 encoding to handle Unicode characters
            import io
            if hasattr(sys.stdout, 'buffer'):
                # Use UTF-8 encoding for console output on Windows
                console_stream = io.TextIOWrapper(
                    sys.stdout.buffer,
                    encoding='utf-8',
                    errors='replace',  # Replace unencodable chars instead of crashing
                    line_buffering=True
                )
            else:
                console_stream = sys.stdout

            logger.add(
                console_stream,
                format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
                level=settings.LOG_LEVEL,
                colorize=True,
                catch=True  # Prevent logger from crashing the app
            )
    except Exception:
        # If console logging fails, continue without it
        pass

    # Ensure at least one handler exists
    if not logger._core.handlers:
        # Add a minimal file logger as fallback
        try:
            fallback_log = Path("logs/fallback.log")
            fallback_log.parent.mkdir(parents=True, exist_ok=True)
            logger.add(
                fallback_log,
                format="{time} | {level} | {message}",
                level="INFO",
                encoding="utf-8",
                catch=True
            )
        except Exception:
            # If all logging fails, use a dummy logger that discards messages
            logger.add(lambda _: None, level=settings.LOG_LEVEL)

    return logger


# Initialize logger
app_logger = setup_logger()
