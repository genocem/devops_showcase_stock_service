"""
Centralized logging configuration for Stock Service
"""
import logging
import sys
import os
from datetime import datetime
from typing import Optional


def setup_logger(name: str = "stock_service") -> logging.Logger:
    """
    Set up and configure the logger for the stock service.

    Args:
        name: Logger name (default: stock_service)

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)

    # Avoid adding handlers multiple times
    if logger.handlers:
        return logger

    # Set log level from environment or default to INFO
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    logger.setLevel(getattr(logging, log_level, logging.INFO))

    # Create formatter with timestamp, level, and context
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler (optional, based on environment)
    log_file = os.getenv("LOG_FILE")
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


# Create default logger instance
logger = setup_logger()


def log_request(endpoint: str, method: str, data: Optional[dict] = None):
    """Log incoming API requests"""
    logger.info(f"REQUEST  | {method} {endpoint} | data={data}")


def log_response(endpoint: str, method: str, status_code: int, success: bool):
    """Log API responses"""
    status = "SUCCESS" if success else "FAILURE"
    logger.info(f"RESPONSE | {method} {endpoint} | status={status_code} | {status}")


def log_celery_task(task_name: str, args: Optional[list] = None, action: str = "RECEIVED"):
    """Log Celery task events"""
    logger.info(f"CELERY   | {action} | task={task_name} | args={args}")


def log_db_operation(operation: str, collection: str, doc_id: Optional[str] = None, success: bool = True):
    """Log database operations"""
    status = "SUCCESS" if success else "FAILURE"
    logger.debug(f"DATABASE | {operation} | collection={collection} | id={doc_id} | {status}")


def log_error(context: str, error: Exception, extra: Optional[dict] = None):
    """Log errors with context"""
    logger.error(f"ERROR    | {context} | error={type(error).__name__}: {str(error)} | extra={extra}")


def log_warning(context: str, message: str, extra: Optional[dict] = None):
    """Log warnings"""
    logger.warning(f"WARNING  | {context} | {message} | extra={extra}")


def log_stock_change(product_id: str, operation: str, amount: int, available: int, reserved: int):
    """Log stock level changes"""
    logger.info(f"STOCK    | {operation} | product={product_id} | amount={amount} | available={available} | reserved={reserved}")
