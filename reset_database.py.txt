import os
import sqlite3
from werkzeug.security import generate_password_hash

def reset_database():
    print("RESETTING DATABASE AND CREATING NEW ADMIN...")
    
    # Delete existing database
    if os.path.exists('corner_door.db'):
        os.remove('corner_door.db')
        print("Old database deleted")
    
    # Create new database with proper structure
    conn = sqlite3.connect('corner_door.db')
    cursor = conn.cursor()
    
    # Create tables
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
    
    # Create admin user
    cursor.execute('''
        INSERT INTO user (username, password_hash, is_admin, is_active, recovery_phrase)
        VALUES (?, ?, 1, 1, ?)
    ''', ('admin', generate_password_hash('admin123'), 'initial admin account'))
    
    # Create sample product
    cursor.execute('''
        INSERT INTO product (title, description, price_usd, crypto_type, admin_rating)
        VALUES (?, ?, ?, ?, ?)
    ''', ('Sample Product', 'This is a sample product for testing', 100.0, 'BTC', 5))
    
    # Create sample wallet
    cursor.execute('''
        INSERT INTO wallet (crypto_type, address)
        VALUES (?, ?)
    ''', ('BTC', '1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa'))
    
    conn.commit()
    conn.close()
    
    print("✅ Database reset complete!")
    print("✅ Admin account created:")
    print("   Username: admin")
    print("   Password: admin123")
    print("✅ Sample product and wallet added")

if __name__ == '__main__':
    reset_database()