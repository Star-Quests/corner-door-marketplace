import os
import sqlite3
from werkzeug.security import generate_password_hash

def reset_with_categories():
    print("🔄 RESETTING DATABASE WITH CATEGORIES...")
    
    # Delete existing database
    if os.path.exists('corner_door.db'):
        os.remove('corner_door.db')
        print("✅ Old database deleted")
    
    # Create new database with proper structure
    conn = sqlite3.connect('corner_door.db')
    cursor = conn.cursor()
    
    # Create tables with category support
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
        CREATE TABLE category (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(50) UNIQUE NOT NULL,
            description TEXT,
            is_active BOOLEAN DEFAULT TRUE,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
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
            allow_user_ratings BOOLEAN DEFAULT TRUE,
            category_id INTEGER,
            FOREIGN KEY (category_id) REFERENCES category (id)
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
    
    # Create admin user
    cursor.execute('''
        INSERT INTO user (username, password_hash, is_admin, is_active, recovery_phrase)
        VALUES (?, ?, 1, 1, ?)
    ''', ('corner', generate_password_hash('cornerdooradmin4life'), 'primary admin account'))
    
    # Create sample categories
    cursor.execute('''
        INSERT INTO category (name, description)
        VALUES (?, ?)
    ''', ('Books', 'Digital and physical books'))
    
    cursor.execute('''
        INSERT INTO category (name, description)
        VALUES (?, ?)
    ''', ('Electronics', 'Gadgets and electronic devices'))
    
    cursor.execute('''
        INSERT INTO category (name, description)
        VALUES (?, ?)
    ''', ('Digital Products', 'Software, courses, and digital content'))
    
    # Create sample products with categories
    cursor.execute('''
        INSERT INTO product (title, description, price_usd, crypto_type, admin_rating, category_id)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', ('Premium Digital Product', 'High-quality digital product with instant delivery', 99.99, 'BTC', 5, 3))
    
    cursor.execute('''
        INSERT INTO product (title, description, price_usd, crypto_type, admin_rating, category_id)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', ('Advanced Crypto Course', 'Master cryptocurrency trading and investment', 199.99, 'ETH', 5, 3))
    
    cursor.execute('''
        INSERT INTO product (title, description, price_usd, crypto_type, admin_rating, category_id)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', ('Wireless Earbuds', 'High-quality wireless earbuds with noise cancellation', 79.99, 'SOL', 4, 2))
    
    # Create sample wallet
    cursor.execute('''
        INSERT INTO wallet (crypto_type, address)
        VALUES (?, ?)
    ''', ('BTC', 'bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh'))
    
    conn.commit()
    conn.close()
    
    print("✅ DATABASE RESET COMPLETE!")
    print("✅ Categories and products with categories added!")
    print("🔑 Admin: corner / cornerdooradmin4life")

if __name__ == '__main__':
    reset_with_categories()