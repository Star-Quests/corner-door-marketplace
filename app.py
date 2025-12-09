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
import warnings

# Suppress SQLAlchemy warnings about missing columns
warnings.filterwarnings('ignore', message="Could not reflect")

app = Flask(__name__)
app.config['SECRET_KEY'] = 'corner-door-ultimate-fix-2024'

# PostgreSQL Configuration
if os.environ.get('DATABASE_URL'):
    # Production - use PostgreSQL
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL').replace('postgres://', 'postgresql://')
else:
    # Development - use SQLite
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///corner_door.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['PRODUCT_DELIVERY_FOLDER'] = 'static/deliveries'
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024

db = SQLAlchemy(app)

# Force create tables in PostgreSQL
with app.app_context(): 
    db.create_all()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

# ========== CLOUDINARY CONFIGURATION (YOUR CREDENTIALS) ==========
CLOUDINARY_CONFIG = {
    'cloud_name': 'dbid7awex',
    'api_key': '456483999232533',
    'api_secret': 'v4gx1Xhfxjll0ES_qUdBygOQrXU',
    'secure': True
}

def init_cloudinary():
    """Initialize Cloudinary if available"""
    try:
        import cloudinary
        import cloudinary.uploader
        import cloudinary.api
        
        cloudinary.config(**CLOUDINARY_CONFIG)
        print("✅ Cloudinary initialized with your account: dbid7awex")
        return True
    except ImportError:
        print("⚠️ Cloudinary not installed. Images will be saved locally.")
        return False
    except Exception as e:
        print(f"⚠️ Cloudinary error: {e}. Using local storage.")
        return False

# Initialize Cloudinary
CLOUDINARY_AVAILABLE = init_cloudinary()

def upload_to_cloudinary(file, folder="products"):
    """Upload file to Cloudinary if available"""
    if not CLOUDINARY_AVAILABLE:
        return None
    
    try:
        import cloudinary.uploader
        upload_result = cloudinary.uploader.upload(
            file,
            folder=f"corner_door/{folder}",
            resource_type="auto"
        )
        return upload_result['secure_url']
    except:
        return None

# ========== DATABASE MODELS (SAFE VERSION) ==========
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
    
    def get_or_create_cart(self):
        cart = Cart.query.filter_by(user_id=self.id).first()
        if not cart:
            cart = Cart(user_id=self.id)
            db.session.add(cart)
            db.session.commit()
        return cart
    
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    products = db.relationship('Product', backref='category', lazy=True)

    def __repr__(self):
        return f'<Category {self.name}>'

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    price_usd = db.Column(db.Float, nullable=False)
    crypto_type = db.Column(db.String(10), nullable=False)
    image_filename = db.Column(db.String(200))
    image_url = db.Column(db.String(500), nullable=True)  # NEW: Optional Cloudinary URL
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    admin_rating = db.Column(db.Integer, default=5)
    allow_user_ratings = db.Column(db.Boolean, default=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=True)
    
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
    delivery_file_url = db.Column(db.String(500), nullable=True)  # NEW: Optional Cloudinary URL
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

# ========== HELPER FUNCTIONS ==========
@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

def get_crypto_prices():
    """Get crypto prices with fallback to defaults"""
    try:
        from crypto_prices import price_manager
        return price_manager.get_prices()
    except:
        return {'BTC': 50000.0, 'ETH': 3000.0, 'SOL': 100.0}

def usd_to_crypto(usd_amount, crypto_type):
    prices = get_crypto_prices()
    crypto_price = prices.get(crypto_type, 1)
    return usd_amount / crypto_price

@app.context_processor
def utility_processor():
    return dict(usd_to_crypto=usd_to_crypto)

def create_notification(user_id, message, order_id=None):
    notification = Notification(
        user_id=user_id,
        message=message,
        order_id=order_id
    )
    db.session.add(notification)
    
    user = db.session.get(User, user_id)
    if user:
        user.unread_notifications = Notification.query.filter_by(user_id=user_id, is_read=False).count()
    db.session.commit()

def hash_ip(ip_address):
    return hashlib.sha256(ip_address.encode()).hexdigest()

def allowed_file(filename, delivery=False):
    if delivery:
        allowed_extensions = {'pdf', 'doc', 'docx', 'txt', 'zip', 'rar', 'mp4', 'avi', 'mov', 'jpg', 'jpeg', 'png', 'gif'}
    else:
        allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

def get_image_url(product):
    """Safely get image URL - prefers Cloudinary, falls back to local"""
    # Try Cloudinary URL first
    if product.image_url:
        return product.image_url
    
    # Fall back to local file
    if product.image_filename:
        return f"/{app.config['UPLOAD_FOLDER']}/{product.image_filename}"
    
    return None

def get_delivery_url(order):
    """Get delivery file URL - FIXED VERSION"""
    print(f"DEBUG get_delivery_url for order #{order.id}:")
    print(f"  delivery_file_url: {order.delivery_file_url}")
    print(f"  delivery_file: {order.delivery_file}")
    
    # Try Cloudinary URL first
    if order.delivery_file_url:
        # Make sure URL has https://
        url = str(order.delivery_file_url)
        if url.startswith('http'):
            print(f"  Returning Cloudinary URL: {url}")
            return url
        elif url.startswith('//'):
            url = 'https:' + url
            print(f"  Fixed protocol, returning: {url}")
            return url
        else:
            print(f"  Returning as-is: {url}")
            return url
    
    # Fall back to local file
    if order.delivery_file:
        # Make sure it's a proper path
        file_path = str(order.delivery_file)
        print(f"  Returning local file: {file_path}")
        return file_path
    
    print("  No delivery file available")
    return None

def save_product_image(file):
    """Save product image - tries Cloudinary first, falls back to local"""
    if not file or file.filename == '':
        return None, None
    
    if allowed_file(file.filename):
        # Try Cloudinary first
        cloudinary_url = upload_to_cloudinary(file, folder="products")
        if cloudinary_url:
            return cloudinary_url, None  # Return URL, no filename
        
        # Fallback to local storage
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        return None, filename  # Return no URL, but filename
    
    return None, None

def save_delivery_file(file, order_id):
    """Save delivery file - tries Cloudinary first, falls back to local"""
    if not file or file.filename == '':
        return None, None
    
    if allowed_file(file.filename, delivery=True):
        # Try Cloudinary first
        cloudinary_url = upload_to_cloudinary(file, folder="deliveries")
        if cloudinary_url:
            return cloudinary_url, None  # Return URL, no path
        
        # Fallback to local storage
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['PRODUCT_DELIVERY_FOLDER'], f"order_{order_id}_{filename}")
        file.save(file_path)
        return None, file_path  # Return no URL, but file path
    
    return None, None

# ========== DATABASE MIGRATION ==========
# ========== DATABASE MIGRATION ==========
def migrate_database_safely():
    """Add missing columns without breaking existing data - PostgreSQL compatible"""
    with app.app_context():
        try:
            from sqlalchemy import inspect, text
            
            inspector = inspect(db.engine)
            
            # Check for image_url column in product table
            product_columns = [col['name'] for col in inspector.get_columns('product')]
            if 'image_url' not in product_columns:
                print("🔄 Adding product.image_url column...")
                conn = db.engine.connect()
                conn.execute(text("ALTER TABLE product ADD COLUMN image_url VARCHAR(500)"))
                conn.commit()
                conn.close()
                print("✅ Added product.image_url column")
            else:
                print("ℹ️ product.image_url column already exists")
            
            # Check for delivery_file_url column in order table
            # Note: order is a reserved word in PostgreSQL, need quotes
            order_columns = [col['name'] for col in inspector.get_columns('order')]
            if 'delivery_file_url' not in order_columns:
                print("🔄 Adding order.delivery_file_url column...")
                conn = db.engine.connect()
                conn.execute(text("""ALTER TABLE "order" ADD COLUMN delivery_file_url VARCHAR(500)"""))
                conn.commit()
                conn.close()
                print("✅ Added order.delivery_file_url column")
            else:
                print("ℹ️ order.delivery_file_url column already exists")
            
            # Also check for the other columns that might be missing
            user_columns = [col['name'] for col in inspector.get_columns('user')]
            if 'unread_notifications' not in user_columns:
                print("🔄 Adding user.unread_notifications column...")
                conn = db.engine.connect()
                conn.execute(text("ALTER TABLE \"user\" ADD COLUMN unread_notifications INTEGER DEFAULT 0"))
                conn.commit()
                conn.close()
                print("✅ Added user.unread_notifications column")
            
            if 'unread_messages' not in user_columns:
                print("🔄 Adding user.unread_messages column...")
                conn = db.engine.connect()
                conn.execute(text("ALTER TABLE \"user\" ADD COLUMN unread_messages INTEGER DEFAULT 0"))
                conn.commit()
                conn.close()
                print("✅ Added user.unread_messages column")
                
        except Exception as e:
            print(f"⚠️ Database migration error: {e}")
            print("⚠️ Try manual SQL fix:")
            print("   psql $DATABASE_URL -c \"ALTER TABLE product ADD COLUMN IF NOT EXISTS image_url VARCHAR(500);\"")
            print("   psql $DATABASE_URL -c \"ALTER TABLE \\\"order\\\" ADD COLUMN IF NOT EXISTS delivery_file_url VARCHAR(500);\"")

# ========== INITIALIZATION ==========
with app.app_context():
    # First migrate database
    migrate_database_safely()
    
    # Then create all tables (for new tables)
    db.create_all()
    print('✅ Database tables verified')
    
    # Create folders
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['PRODUCT_DELIVERY_FOLDER'], exist_ok=True)
    
    # Create admin user if doesn't exist
    if not User.query.filter_by(username='corner').first():
        admin = User(
            username='corner',
            password_hash=generate_password_hash('cornerdooradmin4life'),
            is_admin=True,
            is_active=True
        )
        db.session.add(admin)
        db.session.commit()
        print("✅ Admin user created")

# ========== ROUTES ==========
@app.route('/')
def index():
    products = Product.query.filter_by(is_active=True).all()
    prices = get_crypto_prices()
    return render_template('index.html', products=products, crypto_prices=prices, get_image_url=get_image_url)

@app.route('/crypto-prices')
def crypto_prices_api():
    prices = get_crypto_prices()
    return jsonify(prices)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'error')
            return redirect(url_for('register'))
        
        import random
        recovery_words = ['corner', 'door', 'market', 'secure', 'private', 'crypto']
        recovery_phrase = ' '.join(random.sample(recovery_words, 4))
        
        user = User(
            username=username,
            password_hash=generate_password_hash(password),
            recovery_phrase=recovery_phrase,
            ip_hash=hash_ip(request.remote_addr)
        )
        
        db.session.add(user)
        db.session.commit()
        
        flash(f'Account created! Your recovery phrase: {recovery_phrase} - Save this!', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            if not user.is_active:
                flash('This account has been deactivated.', 'error')
                return redirect(url_for('login'))
            
            login_user(user)
            flash(f'Welcome back, {username}!', 'success')
            
            if user.is_admin:
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('index'))
        else:
            flash('Login failed. Check your username and password.', 'error')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out successfully.', 'success')
    return redirect(url_for('index'))

@app.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    if request.method == 'POST':
        current_password = request.form['current_password']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']
        
        if not check_password_hash(current_user.password_hash, current_password):
            flash('Current password is incorrect', 'error')
            return redirect(url_for('change_password'))
        
        if new_password != confirm_password:
            flash('New passwords do not match', 'error')
            return redirect(url_for('change_password'))
        
        if len(new_password) < 6:
            flash('Password must be at least 6 characters long', 'error')
            return redirect(url_for('change_password'))
        
        current_user.password_hash = generate_password_hash(new_password)
        db.session.commit()
        
        flash('Password changed successfully!', 'success')
        return redirect(url_for('index'))
    
    return render_template('change_password.html')

@app.route('/notifications')
@login_required
def notifications():
    user_notifications = Notification.query.filter_by(user_id=current_user.id).order_by(Notification.created_at.desc()).all()
    for notification in user_notifications:
        if not notification.is_read:
            notification.is_read = True
    current_user.unread_notifications = 0
    db.session.commit()
    
    return render_template('notifications.html', notifications=user_notifications)

@app.route('/notifications/count')
@login_required
def notifications_count():
    return jsonify({'count': current_user.unread_notifications})

@app.route('/chat', methods=['GET', 'POST'])
@login_required
def chat():
    if request.method == 'POST':
        message = request.form['message']
        if message.strip():
            chat_message = ChatMessage(
                user_id=current_user.id,
                message=message.strip(),
                is_admin_reply=False
            )
            db.session.add(chat_message)
            
            admin_user = User.query.filter_by(is_admin=True, is_active=True).first()
            if admin_user:
                admin_user.unread_messages = ChatMessage.query.filter_by(is_read=False, is_admin_reply=False).count()
                create_notification(
                    admin_user.id,
                    f'💬 New message from {current_user.username}: {message[:50]}...',
                    None
                )
            
            db.session.commit()
            flash('Message sent to admin!', 'success')
        
        return redirect(url_for('chat'))
    
    messages = ChatMessage.query.filter(
        (ChatMessage.user_id == current_user.id) | 
        (ChatMessage.is_admin_reply == True)
    ).order_by(ChatMessage.created_at.asc()).all()
    
    for message in messages:
        if not message.is_read and (message.is_admin_reply or message.user_id == current_user.id):
            message.is_read = True
    
    current_user.unread_messages = 0
    db.session.commit()
    
    return render_template('chat.html', messages=messages)

@app.route('/chat/send', methods=['POST'])
@login_required
def send_chat_message():
    message = request.json.get('message', '').strip()
    if not message:
        return jsonify({'error': 'Message cannot be empty'}), 400
    
    chat_message = ChatMessage(
        user_id=current_user.id,
        message=message,
        is_admin_reply=False
    )
    db.session.add(chat_message)
    
    admin_user = User.query.filter_by(is_admin=True, is_active=True).first()
    if admin_user:
        admin_user.unread_messages = ChatMessage.query.filter_by(is_read=False, is_admin_reply=False).count()
    
    db.session.commit()
    
    return jsonify({'success': True, 'message': message})

@app.route('/admin/chat')
@login_required
def admin_chat():
    if not current_user.is_admin:
        flash('Access denied', 'error')
        return redirect(url_for('index'))
    
    user_messages = db.session.query(
        User.id, 
        User.username,
        db.func.max(ChatMessage.created_at).label('last_message')
    ).join(ChatMessage, User.id == ChatMessage.user_id).group_by(User.id, User.username).order_by(db.desc('last_message')).all()
    
    selected_user_id = request.args.get('user_id')
    messages = []
    
    if selected_user_id:
        messages = ChatMessage.query.filter(
            (ChatMessage.user_id == selected_user_id) | 
            (ChatMessage.is_admin_reply == True)
        ).order_by(ChatMessage.created_at.asc()).all()
        
        for message in messages:
            if not message.is_read:
                message.is_read = True
        
        db.session.commit()
    
    unread_counts = {}
    for user_id, username, _ in user_messages:
        unread_counts[user_id] = ChatMessage.query.filter_by(
            user_id=user_id, 
            is_read=False, 
            is_admin_reply=False
        ).count()
    
    return render_template('admin/chat.html', 
                         user_messages=user_messages,
                         messages=messages,
                         selected_user_id=selected_user_id,
                         unread_counts=unread_counts)

@app.route('/admin/chat/reply', methods=['POST'])
@login_required
def admin_chat_reply():
    if not current_user.is_admin:
        return jsonify({'error': 'Access denied'}), 403
    
    user_id = request.json.get('user_id')
    message = request.json.get('message', '').strip()
    
    if not user_id or not message:
        return jsonify({'error': 'User ID and message are required'}), 400
    
    chat_message = ChatMessage(
        user_id=user_id,
        message=message,
        is_admin_reply=True
    )
    db.session.add(chat_message)
    
    user = User.query.get(user_id)
    if user:
        user.unread_messages = ChatMessage.query.filter_by(user_id=user_id, is_read=False, is_admin_reply=True).count()
        create_notification(
            user_id,
            f'💬 Admin replied to your message: {message[:50]}...',
            None
        )
    
    db.session.commit()
    
    return jsonify({'success': True})

@app.route('/chat/messages')
@login_required
def get_chat_messages():
    messages = ChatMessage.query.filter(
        (ChatMessage.user_id == current_user.id) | 
        (ChatMessage.is_admin_reply == True)
    ).order_by(ChatMessage.created_at.asc()).all()
    
    for message in messages:
        if not message.is_read and (message.is_admin_reply or message.user_id == current_user.id):
            message.is_read = True
    
    current_user.unread_messages = 0
    db.session.commit()
    
    messages_data = []
    for msg in messages:
        messages_data.append({
            'id': msg.id,
            'message': msg.message,
            'is_admin_reply': msg.is_admin_reply,
            'created_at': msg.created_at.strftime('%Y-%m-%d %H:%M'),
            'username': msg.user.username if not msg.is_admin_reply else 'Admin'
        })
    
    return jsonify({'messages': messages_data})

@app.route('/cart')
@login_required
def view_cart():
    cart = current_user.get_or_create_cart()
    prices = get_crypto_prices()
    
    total_usd = 0
    cart_items = []
    
    for item in cart.items:
        product_total = item.product.price_usd * item.quantity
        total_usd += product_total
        cart_items.append({
            'item': item,
            'product_total': product_total,
            'crypto_amounts': {
                'BTC': usd_to_crypto(item.product.price_usd, 'BTC'),
                'ETH': usd_to_crypto(item.product.price_usd, 'ETH'),
                'SOL': usd_to_crypto(item.product.price_usd, 'SOL')
            }
        })
    
    crypto_totals = {}
    for crypto in ['BTC', 'ETH', 'SOL']:
        crypto_totals[crypto] = usd_to_crypto(total_usd, crypto)
    
    return render_template('cart.html', 
                         cart_items=cart_items,
                         total_usd=total_usd,
                         crypto_totals=crypto_totals,
                         crypto_prices=prices,
                         get_image_url=get_image_url)

@app.route('/cart/add/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    product = Product.query.get_or_404(product_id)
    cart = current_user.get_or_create_cart()
    
    cart_item = CartItem.query.filter_by(cart_id=cart.id, product_id=product_id).first()
    
    if cart_item:
        cart_item.quantity += 1
    else:
        cart_item = CartItem(cart_id=cart.id, product_id=product_id)
        db.session.add(cart_item)
    
    cart.updated_at = datetime.utcnow()
    db.session.commit()
    
    flash(f'{product.title} added to cart!', 'success')
    return redirect(request.referrer or url_for('index'))

@app.route('/cart/update/<int:item_id>', methods=['POST'])
@login_required
def update_cart_item(item_id):
    cart_item = CartItem.query.get_or_404(item_id)
    
    if cart_item.cart.user_id != current_user.id:
        flash('Access denied', 'error')
        return redirect(url_for('view_cart'))
    
    action = request.form.get('action')
    
    if action == 'increase':
        cart_item.quantity += 1
    elif action == 'decrease' and cart_item.quantity > 1:
        cart_item.quantity -= 1
    elif action == 'remove':
        db.session.delete(cart_item)
    
    db.session.commit()
    flash('Cart updated!', 'success')
    return redirect(url_for('view_cart'))

@app.route('/cart/clear', methods=['POST'])
@login_required
def clear_cart():
    cart = current_user.get_or_create_cart()
    
    CartItem.query.filter_by(cart_id=cart.id).delete()
    cart.updated_at = datetime.utcnow()
    db.session.commit()
    
    flash('Cart cleared!', 'success')
    return redirect(url_for('view_cart'))

@app.route('/cart/checkout', methods=['POST'])
@login_required
def checkout_cart():
    cart = current_user.get_or_create_cart()
    
    if not cart.items:
        flash('Your cart is empty!', 'error')
        return redirect(url_for('view_cart'))
    
    crypto_type = request.form['crypto_type']
    delivery_location = request.form['delivery_location']
    
    wallet = Wallet.query.filter_by(crypto_type=crypto_type, is_active=True).first()
    if not wallet:
        flash('No wallet available for selected cryptocurrency', 'error')
        return redirect(url_for('view_cart'))
    
    total_usd = sum(item.product.price_usd * item.quantity for item in cart.items)
    crypto_amount = usd_to_crypto(total_usd, crypto_type)
    
    orders = []
    for item in cart.items:
        order = Order(
            user_id=current_user.id,
            product_id=item.product.id,
            crypto_type=crypto_type,
            wallet_address=wallet.address,
            crypto_amount=usd_to_crypto(item.product.price_usd * item.quantity, crypto_type),
            delivery_location=delivery_location
        )
        db.session.add(order)
        orders.append(order)
    
    CartItem.query.filter_by(cart_id=cart.id).delete()
    cart.updated_at = datetime.utcnow()
    db.session.commit()
    
    payment_message = f"""
🎯 ORDER CONFIRMED - READY FOR PAYMENT

💰 Total Amount: {crypto_amount:.8f} {crypto_type}
📦 Items in Order: {len(cart.items)}
🏦 Wallet Address: {wallet.address}

📋 Payment Instructions:
1. Send exactly {crypto_amount:.8f} {crypto_type}
2. To address: {wallet.address}
3. Include transaction fee for faster confirmation
4. Click "I Have Paid" after sending

⚠️ Important:
• Send only {crypto_type} to this address
• Amount must be exact
• Contact support if issues occur

Click this notification to view order details with QR code.
"""
    
    admin_user = User.query.filter_by(is_admin=True, is_active=True).first()
    if admin_user:
        create_notification(
            admin_user.id,
            f'🛒 New cart checkout: {len(cart.items)} items from {current_user.username} - Total: ${total_usd:.2f} USD',
            orders[0].id if orders else None
        )
    
    create_notification(
        current_user.id,
        payment_message.strip(),
        orders[0].id if orders else None
    )
    
    flash('Order placed successfully! Check notifications for complete payment instructions.', 'success')
    return redirect(url_for('order_details', order_id=orders[0].id if orders else 0))

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    prices = get_crypto_prices()
    
    crypto_amounts = {}
    for crypto in ['BTC', 'ETH', 'SOL']:
        crypto_amounts[crypto] = usd_to_crypto(product.price_usd, crypto)
    
    return render_template('product.html', product=product, crypto_amounts=crypto_amounts, crypto_prices=prices, get_image_url=get_image_url)

@app.route('/buy/<int:product_id>', methods=['GET', 'POST'])
@login_required
def buy_product(product_id):
    product = Product.query.get_or_404(product_id)
    prices = get_crypto_prices()
    
    if request.method == 'POST':
        crypto_type = request.form['crypto_type']
        delivery_location = request.form['delivery_location']
        
        wallet = Wallet.query.filter_by(crypto_type=crypto_type, is_active=True).first()
        if not wallet:
            flash('No wallet available for selected cryptocurrency', 'error')
            return redirect(url_for('buy_product', product_id=product_id))
        
        crypto_amount = usd_to_crypto(product.price_usd, crypto_type)
        
        order = Order(
            user_id=current_user.id,
            product_id=product.id,
            crypto_type=crypto_type,
            wallet_address=wallet.address,
            crypto_amount=crypto_amount,
            delivery_location=delivery_location
        )
        
        db.session.add(order)
        db.session.commit()
        
        payment_message = f"""
🎯 ORDER CONFIRMED - READY FOR PAYMENT

🛍️ Product: {product.title}
💰 Amount: {crypto_amount:.8f} {crypto_type}
🏦 Wallet Address: {wallet.address}

📋 Payment Instructions:
1. Send exactly {crypto_amount:.8f} {crypto_type}
2. To address: {wallet.address}
3. Include transaction fee for faster confirmation
4. Click "I Have Paid" after sending

⚠️ Important:
• Send only {crypto_type} to this address
• Amount must be exact
• Contact support if issues occur

Click this notification to view order details with QR code.
"""
        
        admin_user = User.query.filter_by(is_admin=True, is_active=True).first()
        if admin_user:
            create_notification(
                admin_user.id,
                f'🛍️ New order #{order.id} for {product.title} by {current_user.username}',
                order.id
            )
        
        create_notification(
            current_user.id,
            payment_message.strip(),
            order.id
        )
        
        flash('Order placed successfully! Check notifications for complete payment instructions.', 'success')
        return redirect(url_for('order_details', order_id=order.id))
    
    crypto_amounts = {}
    for crypto in ['BTC', 'ETH', 'SOL']:
        crypto_amounts[crypto] = usd_to_crypto(product.price_usd, crypto)
    
    return render_template('buy.html', product=product, crypto_amounts=crypto_amounts, crypto_prices=prices, get_image_url=get_image_url)

@app.route('/order/<int:order_id>')
@login_required
def order_details(order_id):
    order = Order.query.get_or_404(order_id)
    if order.user_id != current_user.id and not current_user.is_admin:
        flash('Access denied', 'error')
        return redirect(url_for('index'))
    
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr_data = f"{order.crypto_type}:{order.wallet_address}?amount={order.crypto_amount}"
    qr.add_data(qr_data)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    qr_code = base64.b64encode(buffer.getvalue()).decode()
    
    return render_template('order.html', order=order, qr_code=qr_code, get_delivery_url=get_delivery_url)

@app.route('/order/<int:order_id>/paid', methods=['POST'])
@login_required
def mark_paid(order_id):
    order = Order.query.get_or_404(order_id)
    if order.user_id != current_user.id:
        flash('Access denied', 'error')
        return redirect(url_for('index'))
    
    order.user_paid = True
    db.session.commit()
    
    admin_user = User.query.filter_by(is_admin=True, is_active=True).first()
    if admin_user:
        create_notification(
            admin_user.id,
            f'💰 User marked order #{order.id} as paid. Please verify {order.crypto_amount:.8f} {order.crypto_type} payment.',
            order.id
        )
    
    create_notification(
        current_user.id,
        f'✅ Payment marked as sent! Admin will verify your {order.crypto_amount:.8f} {order.crypto_type} payment for order #{order.id}.',
        order.id
    )
    
    flash('Payment marked as sent. Admin will verify and deliver your product.', 'success')
    return redirect(url_for('order_details', order_id=order_id))

@app.route('/order/<int:order_id>/rate', methods=['POST'])
@login_required
def rate_order(order_id):
    order = Order.query.get_or_404(order_id)
    if order.user_id != current_user.id:
        return jsonify({'error': 'Access denied'}), 403
    
    if not order.admin_paid:
        return jsonify({'error': 'Order not completed yet'}), 400
    
    if not order.product.allow_user_ratings:
        return jsonify({'error': 'Rating not allowed for this product'}), 400
    
    rating = request.json.get('rating')
    review = request.json.get('review', '')
    
    if not rating:
        return jsonify({'error': 'Rating required'}), 400
    
    order.user_rating = int(rating)
    order.user_review = review
    db.session.commit()
    
    return jsonify({'success': True})

@app.route('/download-delivery/<int:order_id>')
@login_required
def download_delivery(order_id):
    order = Order.query.get_or_404(order_id)
    if order.user_id != current_user.id and not current_user.is_admin:
        flash('Access denied', 'error')
        return redirect(url_for('index'))
    
    delivery_url = get_delivery_url(order)
    if not delivery_url:
        flash('No delivery file available', 'error')
        return redirect(url_for('order_details', order_id=order_id))
    
    try:
        print(f"DEBUG download_delivery: Got URL: {delivery_url}")
        
        # If it's a Cloudinary URL (starts with http), redirect to it
        if delivery_url and delivery_url.startswith('http'):
            print(f"DEBUG: Redirecting to Cloudinary URL")
            return redirect(delivery_url)
        
        # If it's a local file path
        if delivery_url and os.path.exists(delivery_url):
            print(f"DEBUG: Sending local file: {delivery_url}")
            return send_file(delivery_url, as_attachment=True)
        elif delivery_url:
            # Try with static folder path
            static_path = delivery_url.replace('\\', '/')
            if os.path.exists(static_path):
                print(f"DEBUG: Sending static file: {static_path}")
                return send_file(static_path, as_attachment=True)
        
        flash('Delivery file not found. Please contact admin.', 'error')
        return redirect(url_for('order_details', order_id=order_id))
            
    except Exception as e:
        print(f"DEBUG download error: {str(e)}")
        flash(f'Error downloading file: {str(e)}', 'error')
        return redirect(url_for('order_details', order_id=order_id))
# Admin routes
@app.route('/admin')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        flash('Access denied', 'error')
        return redirect(url_for('index'))
    
    stats = {
        'total_orders': Order.query.count(),
        'pending_orders': Order.query.filter_by(admin_paid=False).count(),
        'total_products': Product.query.count(),
        'total_users': User.query.count(),
        'unread_notifications': Notification.query.filter_by(is_read=False, user_id=current_user.id).count(),
        'unread_messages': ChatMessage.query.filter_by(is_read=False, is_admin_reply=False).count()
    }
    
    return render_template('admin/dashboard.html', stats=stats)

@app.route('/admin/products', methods=['GET', 'POST'])
@login_required
def admin_products():
    if not current_user.is_admin:
        flash('Access denied', 'error')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        price_usd = float(request.form['price_usd'])
        crypto_type = request.form['crypto_type']
        admin_rating = int(request.form.get('admin_rating', 5))
        allow_user_ratings = 'allow_user_ratings' in request.form
        
        category_id = request.form.get('category_id') or None

        product = Product(
            title=title,
            description=description,
            price_usd=price_usd,
            crypto_type=crypto_type,
            admin_rating=admin_rating,
            allow_user_ratings=allow_user_ratings,
            category_id=category_id
        )
        
        if 'image' in request.files:
            file = request.files['image']
            if file and allowed_file(file.filename):
                # ENHANCED: Try Cloudinary first, fallback to local
                cloudinary_url, filename = save_product_image(file)
                
                if cloudinary_url:
                    product.image_url = cloudinary_url
                    flash('✅ Product image uploaded to Cloudinary! (Will persist forever)', 'success')
                elif filename:
                    product.image_filename = filename
                    flash('ℹ️ Product image saved locally', 'info')
        
        db.session.add(product)
        db.session.commit()
        flash('Product added successfully', 'success')
        return redirect(url_for('admin_products'))
    
    products = Product.query.all()
    categories = Category.query.filter_by(is_active=True).all()
    return render_template('admin/products.html', products=products, categories=categories, get_image_url=get_image_url)

@app.context_processor
def utility_processor():
    return dict(
        usd_to_crypto=usd_to_crypto,
        get_image_url=get_image_url,
        get_delivery_url=get_delivery_url  # MAKE SURE THIS IS HERE
    )

@app.route('/admin/delete_product/<int:product_id>', methods=['POST'])
@login_required
def admin_delete_product(product_id):
    if not current_user.is_admin:
        return jsonify({'error': 'Access denied'}), 403
    
    try:
        product = Product.query.get_or_404(product_id)
        product_title = product.title
        
        # PostgreSQL-compatible deletion
        orders = Order.query.filter_by(product_id=product_id).all()
        if orders:
            order_ids = [order.id for order in orders]
            Notification.query.filter(Notification.order_id.in_(order_ids)).delete(synchronize_session=False)
        
        Order.query.filter_by(product_id=product_id).delete(synchronize_session=False)
        CartItem.query.filter_by(product_id=product_id).delete(synchronize_session=False)
        db.session.delete(product)
        db.session.commit()
        
        return jsonify({
            'success': True, 
            'message': f'Product "{product_title}" deleted successfully!'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Delete failed: {str(e)}'}), 500

@app.route('/admin/wallets', methods=['GET', 'POST'])
@login_required
def admin_wallets():
    if not current_user.is_admin:
        flash('Access denied', 'error')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        crypto_type = request.form['crypto_type']
        address = request.form['address']
        
        if Wallet.query.filter_by(address=address).first():
            flash('Wallet address already exists', 'error')
            return redirect(url_for('admin_wallets'))
        
        wallet = Wallet(crypto_type=crypto_type, address=address)
        db.session.add(wallet)
        db.session.commit()
        flash('Wallet added successfully', 'success')
        return redirect(url_for('admin_wallets'))
    
    wallets = Wallet.query.all()
    return render_template('admin/wallets.html', wallets=wallets)

@app.route('/admin/delete_wallet/<int:wallet_id>', methods=['POST'])
@login_required
def admin_delete_wallet(wallet_id):
    if not current_user.is_admin:
        return jsonify({'error': 'Access denied'}), 403
    
    wallet = Wallet.query.get_or_404(wallet_id)
    
    if Order.query.filter_by(wallet_address=wallet.address).first():
        return jsonify({'error': 'Cannot delete wallet with existing orders'}), 400
    
    db.session.delete(wallet)
    db.session.commit()
    
    return jsonify({'success': True})

@app.route('/admin/orders')
@login_required
def admin_orders():
    if not current_user.is_admin:
        flash('Access denied', 'error')
        return redirect(url_for('index'))
    
    orders = Order.query.order_by(Order.created_at.desc()).all()
    return render_template('admin/orders.html', orders=orders)

@app.route('/admin/order/<int:order_id>/deliver', methods=['GET', 'POST'])
@login_required
def admin_deliver_order(order_id):
    if not current_user.is_admin:
        flash('Access denied', 'error')
        return redirect(url_for('index'))
    
    order = Order.query.get_or_404(order_id)
    
    if request.method == 'POST':
        delivery_notes = request.form.get('delivery_notes', '')
        
        if 'delivery_file' in request.files:
            file = request.files['delivery_file']
            if file and file.filename != '':
                if allowed_file(file.filename, delivery=True):
                    # ENHANCED: Try Cloudinary first, fallback to local
                    cloudinary_url, file_path = save_delivery_file(file, order_id)
                    
                    if cloudinary_url:
                        order.delivery_file_url = cloudinary_url
                        flash('✅ Delivery file uploaded to Cloudinary! (Will persist forever)', 'success')
                    elif file_path:
                        order.delivery_file = file_path
                        flash('ℹ️ Delivery file saved locally', 'info')
                else:
                    flash('Invalid file type for delivery', 'error')
                    return redirect(url_for('admin_deliver_order', order_id=order_id))
        
        order.delivery_notes = delivery_notes
        order.admin_paid = True
        db.session.commit()
        
        create_notification(
            order.user_id,
            f'🎉 ORDER #{order.id} DELIVERED!\n\nYour product "{order.product.title}" is ready for download.\n\n📥 Click the download link to get your files.\n⭐ Don\'t forget to rate your purchase!',
            order.id
        )
        
        flash('Product delivered successfully!', 'success')
        return redirect(url_for('admin_orders'))
    
    return render_template('admin/deliver_order.html', order=order)

@app.route('/admin/order/<int:order_id>/mark_paid', methods=['POST'])
@login_required
def admin_mark_paid(order_id):
    if not current_user.is_admin:
        return jsonify({'error': 'Access denied'}), 403
    
    order = Order.query.get_or_404(order_id)
    order.admin_paid = True
    db.session.commit()
    
    create_notification(
        order.user_id,
        f'✅ PAYMENT VERIFIED!\n\nYour payment of {order.crypto_amount:.8f} {order.crypto_type} for order #{order.id} has been confirmed.\n\nYour product will be delivered shortly.',
        order.id
    )
    
    return jsonify({'success': True})

@app.route('/admin/users')
@login_required
def admin_users():
    if not current_user.is_admin:
        flash('Access denied', 'error')
        return redirect(url_for('index'))
    
    users = User.query.all()
    return render_template('admin/users.html', users=users)

@app.route('/admin/toggle_user/<int:user_id>', methods=['POST'])
@login_required
def admin_toggle_user(user_id):
    if not current_user.is_admin:
        return jsonify({'error': 'Access denied'}), 403
    
    if user_id == current_user.id:
        return jsonify({'error': 'Cannot deactivate yourself'}), 400
    
    user = User.query.get_or_404(user_id)
    user.is_active = not user.is_active
    db.session.commit()
    
    return jsonify({'success': True, 'is_active': user.is_active})

@app.route('/admin/change_user_password/<int:user_id>', methods=['POST'])
@login_required
def admin_change_user_password(user_id):
    if not current_user.is_admin:
        return jsonify({'error': 'Access denied'}), 403
    
    user = User.query.get_or_404(user_id)
    new_password = request.form['new_password']
    
    if len(new_password) < 6:
        return jsonify({'error': 'Password must be at least 6 characters'})
    
    user.password_hash = generate_password_hash(new_password)
    db.session.commit()
    
    return jsonify({'success': True})

@app.route('/search')
def search():
    query = request.args.get('q', '')
    category_id = request.args.get('category', '')
    
    products_query = Product.query.filter_by(is_active=True)
    
    if query:
        products_query = products_query.filter(
            db.or_(
                Product.title.ilike(f'%{query}%'),
                Product.description.ilike(f'%{query}%')
            )
        )
    
    if category_id:
        products_query = products_query.filter_by(category_id=category_id)
    
    products = products_query.all()
    categories = Category.query.filter_by(is_active=True).all()
    
    return render_template('search.html', 
                         products=products, 
                         categories=categories,
                         search_query=query,
                         selected_category=category_id,
                         get_image_url=get_image_url)

@app.route('/setup-database')
def setup_database():
    """One-time database setup route"""
    try:
        db.create_all()
        
        if not User.query.filter_by(username='corner').first():
            admin = User(
                username='corner',
                password_hash=generate_password_hash('cornerdooradmin4life'),
                is_admin=True,
                is_active=True
            )
            db.session.add(admin)
            db.session.commit()
            return "✅ Database setup complete! Tables and admin user created."
        else:
            return "✅ Database already set up."
            
    except Exception as e:
        return f"❌ Setup failed: {str(e)}"

@app.route('/admin/categories', methods=['GET', 'POST'])
@login_required
def admin_categories():
    if not current_user.is_admin:
        flash('Access denied', 'error')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        
        if Category.query.filter_by(name=name).first():
            flash('Category already exists', 'error')
            return redirect(url_for('admin_categories'))
        
        category = Category(name=name, description=description)
        db.session.add(category)
        db.session.commit()
        flash('Category added successfully!', 'success')
        return redirect(url_for('admin_categories'))
    
    categories = Category.query.all()
    return render_template('admin/categories.html', categories=categories)

@app.route('/admin/delete_category/<int:category_id>', methods=['POST'])
@login_required
def admin_delete_category(category_id):
    if not current_user.is_admin:
        return jsonify({'error': 'Access denied'}), 403
    
    try:
        category = Category.query.get_or_404(category_id)
        
        Product.query.filter_by(category_id=category_id).update({'category_id': None})
        
        db.session.delete(category)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Category deleted successfully!'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to delete category: {str(e)}'}), 500

@app.route('/fix-images')
def fix_images():
    """Check all products and show their image info"""
    products = Product.query.all()
    
    html = "<h1>Product Image Status</h1>"
    
    for product in products:
        html += f"""
        <div style="border: 1px solid #ccc; padding: 10px; margin: 10px;">
            <h3>Product #{product.id}: {product.title}</h3>
            <p>Price: ${product.price_usd}</p>
            <p><strong>Cloudinary URL:</strong> {product.image_url or 'NOT SET'}</p>
            <p><strong>Local Filename:</strong> {product.image_filename or 'NOT SET'}</p>
            <p><strong>Current get_image_url() returns:</strong> {get_image_url(product)}</p>
        </div>
        """
    
    html += "<p>If Cloudinary URL is blank, the image wasn't uploaded to Cloudinary.</p>"
    return html

@app.route('/check-product/<int:product_id>')
def check_product(product_id):
    product = Product.query.get_or_404(product_id)
    
    return f"""
    <h3>Product: {product.title}</h3>
    <p>Image URL: {product.image_url}</p>
    <p>Image Filename: {product.image_filename}</p>
    <hr>
    <p>If you see a Cloudinary URL above, the image should work.</p>
    <p>If not, the image wasn't saved correctly.</p>
    <a href="/admin/products">Back to products</a>
    """

# ========== EMERGENCY DATABASE FIX ==========
@app.route('/fix-database-now')
def fix_database_now():
    """ONE-TIME emergency database fix - run this once then remove"""
    try:
        from sqlalchemy import text
        
        with app.app_context():
            conn = db.engine.connect()
            
            # Add missing columns
            conn.execute(text("""
                ALTER TABLE product 
                ADD COLUMN IF NOT EXISTS image_url VARCHAR(500)
            """))
            
            conn.execute(text("""
                ALTER TABLE "order"
                ADD COLUMN IF NOT EXISTS delivery_file_url VARCHAR(500)
            """))
            
            conn.commit()
            conn.close()
        
        return """
        ✅ DATABASE FIXED!
        
        Columns added:
        1. product.image_url
        2. order.delivery_file_url
        
        Your site should now work perfectly.
        
        <a href="/">Go to homepage</a>
        """
    except Exception as e:
        return f"""
        ❌ FIX FAILED: {str(e)}
        
        Please go to Render Dashboard → Shell and run:
        
        psql $DATABASE_URL -c "ALTER TABLE product ADD COLUMN IF NOT EXISTS image_url VARCHAR(500);"
        psql $DATABASE_URL -c "ALTER TABLE \\"order\\" ADD COLUMN IF NOT EXISTS delivery_file_url VARCHAR(500);"
        """

if __name__ == '__main__':
    print("")
    print("🚀 CORNER DOOR MARKETPLACE STARTED!")
    print("🔑 ADMIN LOGIN:")
    print("   Username: corner")
    print("   Password: cornerdooradmin4life")
    
    if CLOUDINARY_AVAILABLE:
        print("☁️  CLOUDINARY: Enabled with your account (dbid7awex)")
        print("✅ Images will persist forever!")
    else:
        print("⚠️  CLOUDINARY: Not available. Install: pip install cloudinary")
        print("⚠️  Images will be saved locally (may disappear on restart)")
    
    print("🌐 ACCESS AT: http://localhost:5000")
    print("")
    
    app.run(debug=True, port=5000)