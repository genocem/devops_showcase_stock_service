"""
JWT authentication utilities
"""
import jwt
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify, current_app
# from app.models.user import User ------------- thing is idk what will take the user's place cause if we're going for a transaction approach
# then a cart that is not empty will be considered a pending transaction and then we'll have it's id here for jwt 
# but if we're going to have a diffrent model for the cart .... that doesn't seem right
# a pending transaction is the content of a cart 
# i went online and i was wrong a cart is not the same as the transaction 
# ok now how would the cart_service handle the cart 
# like is it gonna have it's own communication with the db or use the api's routes

def generate_token(user_id, expires_in=24):
    """Generate JWT token"""
    user = User.query.get(user_id)
    payload = {
        'user_id': user_id,
        'is_admin': user.is_admin if user else False,
        'exp': datetime.now(datetime.timezone.utc) + timedelta(hours=expires_in),
        'iat': datetime.now(datetime.timezone.utc)
    }
    return jwt.encode(payload, current_app.config['JWT_SECRET_KEY'], algorithm='HS256')

def decode_token(token):
    """Decode and verify JWT token"""
    try:
        payload = jwt.decode(token, current_app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def token_required(f):
    """Decorator to protect routes with JWT"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        
        if not token:
            return jsonify({'error': 'Token missing'}), 401
        
        if token.startswith('Bearer '):
            token = token[7:]
        
        payload = decode_token(token)
        if not payload:
            return jsonify({'error': 'Invalid or expired token'}), 401
        
        current_user = User.query.get(payload['user_id'])
        if not current_user or not current_user.is_active:
            return jsonify({'error': 'User not found or inactive'}), 401
        
        return f(current_user, *args, **kwargs)
    
    return decorated
