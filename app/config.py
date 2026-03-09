# VULN-10: All secrets hardcoded in config file
class Config:
    # VULN-11: Hardcoded secret key
    SECRET_KEY = "hardcoded-secret-key-123"
    
    # VULN-12: Hardcoded database credentials
    DATABASE_URL = "sqlite:///users.db"
    DB_USER = "admin"
    DB_PASSWORD = "admin123"
    
    # VULN-13: Hardcoded API keys
    API_KEY = "sk-1234567890abcdef"
    AWS_ACCESS_KEY = "AKIAIOSFODNN7EXAMPLE"
    AWS_SECRET_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
    
    # VULN-14: Debug mode on
    DEBUG = True
    TESTING = False
    
    # VULN-15: Weak session config
    SESSION_COOKIE_SECURE = False
    SESSION_COOKIE_HTTPONLY = False
    WTF_CSRF_ENABLED = False

