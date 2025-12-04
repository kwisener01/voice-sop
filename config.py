import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Application configuration"""

    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    DEBUG = os.getenv('FLASK_DEBUG', 'False') == 'True'

    # API Keys
    VAPI_API_KEY = os.getenv('VAPI_API_KEY')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    GHL_API_KEY = os.getenv('GHL_API_KEY')

    # Google
    GOOGLE_CREDENTIALS_PATH = os.getenv('GOOGLE_CREDENTIALS_PATH', './credentials/google_credentials.json')
    GOOGLE_FOLDER_ID = os.getenv('GOOGLE_FOLDER_ID')

    # Lindy
    LINDY_WEBHOOK_SECRET = os.getenv('LINDY_WEBHOOK_SECRET')
    LINDY_WEBHOOK_URL = os.getenv('LINDY_WEBHOOK_URL')

    # Database
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///voice_sop.db')

    # Redis
    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')

    # Server
    PORT = int(os.getenv('PORT', 5000))
    HOST = os.getenv('HOST', '0.0.0.0')

    # VAPI Configuration
    VAPI_BASE_URL = 'https://api.vapi.ai'

    # GHL Configuration
    GHL_BASE_URL = 'https://rest.gohighlevel.com/v1'

    @staticmethod
    def validate():
        """Validate required configuration"""
        required = [
            'VAPI_API_KEY',
            'OPENAI_API_KEY',
            'GHL_API_KEY'
        ]
        missing = [key for key in required if not os.getenv(key)]
        if missing:
            raise ValueError(f"Missing required environment variables: {', '.join(missing)}")
