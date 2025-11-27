import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-change-this-in-production-123'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///corner_door.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = 'static/uploads'
    PRODUCT_DELIVERY_FOLDER = 'static/deliveries'
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50MB max file size