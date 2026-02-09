"""
Utils package initialization
"""
from app.utils.decorators import validate_json
from app.utils.error_handlers import register_error_handlers

__all__ = ['validate_json', 'register_error_handlers']
