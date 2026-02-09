"""
Utility decorators
"""
from functools import wraps
from flask import request, jsonify

def validate_json(required_fields):
    """Decorator to validate required JSON fields"""
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if not request.is_json:
                return jsonify({'error': 'Content-Type must be application/json'}), 400
            
            data = request.get_json()
            missing_fields = [field for field in required_fields if field not in data]
            
            if missing_fields:
                return jsonify({
                    'error': f"Missing required fields: {', '.join(missing_fields)}"
                }), 400
            
            return f(*args, **kwargs)
        return wrapper
    return decorator

def admin_required(f):
    """Decorator to require admin role"""
    @wraps(f)
    def wrapper(current_user, *args, **kwargs):
        if not current_user.is_admin:
            return jsonify({'error': 'Admin access required'}), 403
        return f(current_user, *args, **kwargs)
    return wrapper
