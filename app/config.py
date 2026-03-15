"""
Configuration settings for different environments
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')

    MONGODB_DB= os.getenv('MONGODB_DB', 'devopsshowcase')
    MONGODB_HOST=os.getenv('MONGODB_HOST', 'localhost')
    MONGODB_PORT=os.getenv('MONGODB_PORT', '27017')
    MONGODB_USER=os.getenv('MONGODB_USERNAME')
    MONGODB_PASSWORD=os.getenv('MONGODB_PASSWORD')
    MONGODB_AUTH_SOURCE=os.getenv('MONGODB_AUTH_SOURCE', 'devopsshowcase')

    # Security
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False

class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True

config_by_name = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}
