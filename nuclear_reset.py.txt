import os
import sqlite3
from werkzeug.security import generate_password_hash

def nuclear_reset():
    print("💥 NUCLEAR DATABASE RESET...")
    print("=" * 50)
    
    # Delete ALL database files
    db_files = ['corner_door.db', 'instance/corner_door.db', 'corner_door.db.wal', 'corner_door.db-shm']
    for db_file in db_files:
        if os.path.exists(db_file):
            os.remove(db_file)
            print(f"✅ Deleted: {db_file}")
    
    # Delete instance folder if empty
    try:
        if os.path.exists('instance') and not os.listdir('instance'):
            os.rmdir('instance')
            print("✅ Deleted empty instance folder")
    except:
        pass
    
    # Create fresh database with proper structure
    conn = sqlite3.connect('corner_door.db')
    cursor = conn.cursor()
    
    # Create all tables
    cursor.execute('''
        CREATE TABLE user (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username VARCHAR(80) UNIQUE NOT NULL,
            password_hash VARCHAR(120) NOT NULL,
            recovery_phrase VARCHAR(200),
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            is_active BOOLEAN DEFAULT TRUE,
            is_admin BOOLEAN DEFAULT FALSE,
            ip_hash VARCHAR(64),
            unread_notifications INTEGER DEFAULT 0
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE product (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title VARCHAR(200) NOT NULL,
            description TEXT,
            price_usd FLOAT NOT NULL,
            crypto_type VARCHAR(10) NOT NULL,
            image_filename VARCHAR(200),
            is_active BOOLEAN DEFAULT TRUE,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            admin_rating INTEGER DEFAULT 5,
            allow_user_ratings BOOLEAN DEFAULT TRUE
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE wallet (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            crypto_type VARCHAR(10) NOT NULL,
            address VARCHAR(200) NOT NULL,
            is_active BOOLEAN DEFAULT TRUE
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE "order" (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            crypto_type VARCHAR(10) NOT NULL,
            wallet_address VARCHAR(200) NOT NULL,
            crypto_amount FLOAT,
            user_paid BOOLEAN DEFAULT FALSE,
            admin_paid BOOLEAN DEFAULT FALSE,
            delivery_location TEXT,
            delivery_file VARCHAR(500),
            delivery_notes TEXT,
            user_rating INTEGER,
            user_review TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES user (id),
            FOREIGN KEY (product_id) REFERENCES product (id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE notification (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            message TEXT NOT NULL,
            is_read BOOLEAN DEFAULT FALSE,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            order_id INTEGER,
            FOREIGN KEY (user_id) REFERENCES user (id),
            FOREIGN KEY (order_id) REFERENCES "order" (id)
        )
    ''')
    
    # CART TABLES
    cursor.execute('''
        CREATE TABLE cart (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES user (id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE cart_item (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cart_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER DEFAULT 1,
            added_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (cart_id) REFERENCES cart (id),
            FOREIGN KEY (product_id) REFERENCES product (id),
            UNIQUE(cart_id, product_id)
        )
    ''')
    
    # Create the admin account
    username = "corner"
    password = "cornerdooradmin4life"
    
    cursor.execute('''
        INSERT INTO user (username, password_hash, is_admin, is_active, recovery_phrase)
        VALUES (?, ?, 1, 1, ?)
    ''', (username, generate_password_hash(password), 'nuclear reset admin'))
    
    # Create backup admins
    cursor.execute('''
        INSERT INTO user (username, password_hash, is_admin, is_active, recovery_phrase)
        VALUES (?, ?, 1, 1, ?)
    ''', ('admin', generate_password_hash('admin123'), 'backup admin 1'))
    
    cursor.execute('''
        INSERT INTO user (username, password_hash, is_admin, is_active, recovery_phrase)
        VALUES (?, ?, 1, 1, ?)
    ''', ('superadmin', generate_password_hash('superadmin123'), 'backup admin 2'))
    
    # Create sample products
    cursor.execute('''
        INSERT INTO product (title, description, price_usd, crypto_type, admin_rating)
        VALUES (?, ?, ?, ?, ?)
    ''', ('Premium Digital Product', 'High-quality digital product with instant delivery', 99.99, 'BTC', 5))
    
    cursor.execute('''
        INSERT INTO product (title, description, price_usd, crypto_type, admin_rating)
        VALUES (?, ?, ?, ?, ?)
    ''', ('Advanced Crypto Course', 'Master cryptocurrency trading and investment', 199.99, 'ETH', 5))
    
    cursor.execute('''
        INSERT INTO product (title, description, price_usd, crypto_type, admin_rating)
        VALUES (?, ?, ?, ?, ?)
    ''', ('NFT Art Collection', 'Limited edition digital artwork', 79.99, 'SOL', 4))
    
    cursor.execute('''
        INSERT INTO product (title, description, price_usd, crypto_type, admin_rating)
        VALUES (?, ?, ?, ?, ?)
    ''', ('Privacy Tools Bundle', 'Complete privacy and security toolkit', 149.99, 'BTC', 5))
    
    # Create sample wallets
    cursor.execute('''
        INSERT INTO wallet (crypto_type, address)
        VALUES (?, ?)
    ''', ('BTC', 'bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh'))
    
    cursor.execute('''
        INSERT INTO wallet (crypto_type, address)
        VALUES (?, ?)
    ''', ('ETH', '0x742d35Cc6634C0532925a3b8D6B39f4F2A5E8E9C'))
    
    cursor.execute('''
        INSERT INTO wallet (crypto_type, address)
        VALUES (?, ?)
    ''', ('SOL', 'So11111111111111111111111111111111111111112'))
    
    conn.commit()
    
    # Verify everything
    cursor.execute("SELECT username, is_admin, is_active FROM user WHERE username = ?", (username,))
    admin = cursor.fetchone()
    
    cursor.execute("SELECT COUNT(*) FROM product")
    product_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM wallet")
    wallet_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM cart")
    cart_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM cart_item")
    cart_item_count = cursor.fetchone()[0]
    
    conn.close()
    
    print("")
    print("✅ NUCLEAR RESET COMPLETE!")
    print("")
    print("🔑 ADMIN CREDENTIALS:")
    print(f"   👤 Primary: {username} / {password}")
    print("   👤 Backup: admin / admin123")
    print("   👤 Emergency: superadmin / superadmin123")
    print("")
    print("📦 SAMPLE DATA CREATED:")
    print(f"   - {product_count} products")
    print(f"   - {wallet_count} wallet addresses")
    print(f"   - Cart system ready (tables: {cart_count} carts, {cart_item_count} items)")
    print("")
    print("🛒 SHOPPING CART FEATURES:")
    print("   ✅ Add to cart")
    print("   ✅ Update quantities")
    print("   ✅ Remove items")
    print("   ✅ Cart checkout")
    print("   ✅ Multi-crypto support")
    print("")
    print("🚀 NEXT STEPS:")
    print("   1. Run: python app.py")
    print("   2. Go to: http://localhost:5000")
    print("   3. Login with: corner / cornerdooradmin4life")
    print("   4. You should see ADMIN DASHBOARD!")
    print("   5. Test cart functionality by adding products")

if __name__ == '__main__':
    nuclear_reset()