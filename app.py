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
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'corner-door-secret-2024')

# USE EXISTING POSTGRESQL DATABASE
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///corner_door.db').replace('postgres://', 'postgresql://')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['PRODUCT_DELIVERY_FOLDER'] = 'static/deliveries'
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024

db = SQLAlchemy(app)

# AUTO-FIX: Create tables in PostgreSQL
with app.app_context():
    db.create_all()
    print("✅ TABLES CREATED!")
    if not User.query.filter_by(username='corner').first():
        admin=User(username='corner',password_hash=generate_password_hash('cornerdooradmin4life'),is_admin=True,is_active=True,recovery_phrase='primary admin')
        db.session.add(admin)
        db.session.commit()
        print("🎉 ADMIN CREATED")


# ... (ALL YOUR EXISTING CODE REMAINS THE SAME)

