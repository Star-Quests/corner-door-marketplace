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

# Database initialization function (defined early but called later)
def initialize_database():
    with app.app_context():
        print("🔄 CREATING DATABASE TABLES...")
        db.create_all()
        create_first_admin()
        print("✅ DATABASE INITIALIZED!")

# ========== MODEL DEFINITIONS ==========
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    recovery_phrase = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)
    ip_hash = db.Column(db.String(64))
    unread_notifications = db.Column(db.Integer, default=0)
    unread_messages = db.Column(db.Integer, default=0)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    price_usd = db.Column(db.Float, nullable=False)
    crypto_type = db.Column(db.String(10), nullable=False)
    image_filename = db.Column(db.String(200))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    admin_rating = db.Column(db.Integer, default=5)
    allow_user_ratings = db.Column(db.Boolean, default=True)

class Wallet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    crypto_type = db.Column(db.String(10), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    is_active = db.Column(db.Boolean, default=True)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    crypto_type = db.Column(db.String(10), nullable=False)
    wallet_address = db.Column(db.String(200), nullable=False)
    crypto_amount = db.Column(db.Float)
    user_paid = db.Column(db.Boolean, default=False)
    admin_paid = db.Column(db.Boolean, default=False)
    delivery_location = db.Column(db.Text)
    delivery_file = db.Column(db.String(500))
    delivery_notes = db.Column(db.Text)
    user_rating = db.Column(db.Integer)
    user_review = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref='orders')
    product = db.relationship('Product', backref='orders')

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=True)
    
    user = db.relationship('User', backref='notifications')
    order = db.relationship('Order', backref='notifications')

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = db.relationship('User', backref='cart')
    items = db.relationship('CartItem', backref='cart', cascade='all, delete-orphan')

class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey('cart.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    added_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    product = db.relationship('Product', backref='cart_items')

class ChatMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_admin_reply = db.Column(db.Boolean, default=False)
    reply_to = db.Column(db.Integer, db.ForeignKey('chat_message.id'), nullable=True)
    
    user = db.relationship('User', backref='chat_messages')
    replies = db.relationship('ChatMessage', backref=db.backref('parent', remote_side=[id]))

# ========== NOW DEFINE create_first_admin() AFTER MODELS ==========
def create_first_admin():
    if not User.query.filter_by(username='corner').first():
        admin = User(
            username='corner',
            password_hash=generate_password_hash('cornerdooradmin4life'),
            is_admin=True,
            is_active=True,
            recovery_phrase='primary admin account'
        )
        db.session.add(admin)
        db.session.commit()
        print("🎉 PRIMARY ADMIN CREATED: username='corner', password='cornerdooradmin4life'")

# ========== ROUTES AND OTHER FUNCTIONS ==========
@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

# ... [PASTE ALL YOUR EXISTING ROUTES HERE] ...

# ========== APP STARTUP ==========

# ========== BASIC ROUTES TO MAKE WEBSITE WORK ==========

@app.route('/')
def index():
    products = Product.query.filter_by(is_active=True).all()
    # Simple crypto prices fallback
    crypto_prices = {'BTC': 50000.0, 'ETH': 3000.0, 'SOL': 100.0}
    return "🔄 Website is setting up... Database is working! Add your templates."

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return f"✅ Logged in as {username}"
        return "❌ Login failed"
    return "📝 Login page - add your template"

@app.route('/admin')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        return "❌ Access denied"
    return "🛠️ Admin dashboard - add your template"

# Add this function for crypto prices
def get_crypto_prices():
    return {'BTC': 50000.0, 'ETH': 3000.0, 'SOL': 100.0}

# Make function available to templates
@app.context_processor
def utility_processor():
    return dict(usd_to_crypto=lambda usd, crypto: usd / get_crypto_prices().get(crypto, 1))
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

