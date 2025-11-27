import os
import hashlib
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import qrcode
import io
import base64

app = Flask(__name__)
app.config['SECRET_KEY'] = 'corner-door-ultimate-fix-2024'

# PostgreSQL Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///corner_door.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['PRODUCT_DELIVERY_FOLDER'] = 'static/deliveries'
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

# Database initialization function
def initialize_database():
    with app.app_context():
        print("🔄 CREATING DATABASE TABLES...")
        db.create_all()
        create_first_admin()
        print("✅ DATABASE INITIALIZED!")

# REST OF YOUR EXISTING CODE (models, routes, etc.)...
# [PASTE ALL YOUR EXISTING MODELS AND ROUTES HERE]

# At the bottom, replace the main block:
if __name__ == '__main__':
    initialize_database()
    
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['PRODUCT_DELIVERY_FOLDER'], exist_ok=True)
    
    admin = User.query.filter_by(username='corner').first()
    if admin:
        print(f"✅ ADMIN VERIFIED: {admin.username}")
    
    print("🚀 CORNER DOOR MARKETPLACE STARTED!")
    app.run(debug=True, port=5000)
else:
    # For Render deployment
    initialize_database()
