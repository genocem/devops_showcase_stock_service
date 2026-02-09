"""
Configuration settings for different environments
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    # SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key')

    # Database
    # DB_HOST = os.getenv('DB_HOST', 'localhost')
    # DB_PORT = os.getenv('DB_PORT', '5432')
    # DB_NAME = os.getenv('DB_NAME', 'banking_db')
    # DB_USER = os.getenv('DB_USER', 'postgres')
    # DB_PASSWORD = os.getenv('DB_PASSWORD', '')


    MONGODB_DB= os.getenv('MONGODB_DB', 'devopsshowcase')
    MONGODB_HOST=os.getenv('MONGODB_HOST', 'localhost')
    MONGODB_PORT=os.getenv('MONGODB_PORT', '27017')
    MONGODB_USER=os.getenv('MONGODB_USERNAME')
    MONGODB_PASSWORD=os.getenv('MONGODB_PASSWORD')
    MONGODB_AUTH_SOURCE=os.getenv('MONGODB_AUTH_SOURCE', 'devopsshowcase')
    # SQLALCHEMY_DATABASE_URI = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

    # Security
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'

    # Email
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'True') == 'True'
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER')

    # OTP
    OTP_EXPIRY_MINUTES = int(os.getenv('OTP_EXPIRY_MINUTES', 5))
    OTP_LENGTH = int(os.getenv('OTP_LENGTH', 6))

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
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

config_by_name = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}
