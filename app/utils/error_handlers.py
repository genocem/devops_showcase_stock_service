"""
Error handlers for the application
"""
from flask import jsonify, request
from app.utils.logging_config import logger

def register_error_handlers(app):
    """Register error handlers"""

    @app.errorhandler(400)
    def bad_request(error):
        logger.warning(f"Bad request | path={request.path} | method={request.method}")
        return jsonify({'error': 'Bad request'}), 400

    @app.errorhandler(401)
    def unauthorized(error):
        logger.warning(f"Unauthorized access | path={request.path} | method={request.method}")
        return jsonify({'error': 'Unauthorized'}), 401

    @app.errorhandler(403)
    def forbidden(error):
        logger.warning(f"Forbidden access | path={request.path} | method={request.method}")
        return jsonify({'error': 'Forbidden'}), 403

    @app.errorhandler(404)
    def not_found(error):
        logger.warning(f"Resource not found | path={request.path} | method={request.method}")
        return jsonify({'error': 'Resource not found'}), 404

    @app.errorhandler(500)
    def internal_error(error):
        logger.error(f"Internal server error | path={request.path} | method={request.method} | error={str(error)}")
        return jsonify({'error': 'Internal server error'}), 500


