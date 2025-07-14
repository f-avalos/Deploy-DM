import os
from dotenv import load_dotenv

# Load environment variables from .env file for local development
load_dotenv()

class Config:
    """Base configuration class"""
    FLASK_ENV = os.environ.get('FLASK_ENV', 'production')
    DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    MODEL_PATH = os.environ.get('MODEL_PATH', 'best_model.pkl')
    PORT = int(os.environ.get('PORT', 5000))
    
    # Logging configuration
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    
    @staticmethod
    def is_production():
        return Config.FLASK_ENV == 'production'
    
    @staticmethod
    def is_development():
        return Config.FLASK_ENV == 'development'
