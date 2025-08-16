import os

class Config:
    # Configuración de la aplicación
    SECRET_KEY = os.environ.get('SESSION_SECRET', 'dev-secret-key-change-in-production')
    UPLOAD_FOLDER = 'static/uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    
    # Configuración de Gemini API
    # IMPORTANTE: Reemplaza con tu API key real de Google AI Studio
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', 'AIzaSyAa89XOH3tFwyR6-eMM812u_8840YexuHA')
    
    # Configuración de base de datos (para futuras implementaciones)
    DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///app.db')
    
    # Configuración de desarrollo
    DEBUG = os.environ.get('FLASK_ENV') == 'development'
