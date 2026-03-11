import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(32)
    DB_USERNAME = os.environ.get('DB_USERNAME', 'admin')
    DB_PASSWORD = os.environ.get('DB_PASSWORD')
    DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///app.db')
    API_KEY = os.environ.get('API_KEY')
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')

    DEBUG = False
    TESTING = False
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    WTF_CSRF_ENABLED = True
