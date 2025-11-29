import os
import glob
import time
import sqlite3
from app import app, db
from werkzeug.security import generate_password_hash

def force_clean():
    print("💥 FORCE CLEANING DATABASE...")
    
    # Find and remove ALL database files
    db_patterns = [
        'corner_door.db',
        'corner_door.db*',  # This gets wal, shm files
        'instance/corner_door.db',
        'instance/corner_door.db*'
    ]
    
    removed_files = []
    for pattern in db_patterns:
        for file_path in glob.glob(pattern):
            try:
                os.remove(file_path)
                removed_files.append(file_path)
                print(f"✅ Removed: {file_path}")
            except Exception as e:
                print(f"⚠️ Could not remove {file_path}: {e}")
    
    # Wait a moment to ensure files are released
    time.sleep(1)
    
    # Create instance directory if needed
    os.makedirs('instance', exist_ok=True)
    
    print(f"\n📊 Removed {len(removed_files)} database files")
    
    with app.app_context():
        try:
            # Force create all tables
            db.drop_all()  # Drop any existing tables
            db.create_all()  # Create fresh tables
            print("✅ Fresh database tables created!")
            
            # Now create minimal data
            from app import User, Category, Product, Wallet
            
            # Check if admin exists before creating
            existing_admin = User.query.filter_by(username='corner').first()
            if not existing_admin:
                admin = User(
                    username='corner',
                    password_hash=generate_password_hash('cornerdooradmin4life'),
                    is_admin=True,
                    is_active=True,
                    recovery_phrase='force clean admin'
                )
                db.session.add(admin)
                print("✅ Admin user created")
            else:
                print("⚠️ Admin user already exists")
            
            # Create categories
            categories_data = [
                ('Books', 'Digital and physical books'),
                ('Electronics', 'Gadgets and devices'),
                ('Digital Products', 'Software and courses'),
                ('Services', 'Consultations and services')
            ]
            
            for name, description in categories_data:
                existing = Category.query.filter_by(name=name).first()
                if not existing:
                    category = Category(name=name, description=description)
                    db.session.add(category)
                    print(f"✅ Created category: {name}")
                else:
                    print(f"⚠️ Category exists: {name}")
            
            db.session.commit()
            print("✅ Categories committed")
            
            # Create products with categories
            products_data = [
                ('Premium Ebook', 'Collection of ebooks', 49.99, 'BTC', 1),
                ('Wireless Headphones', 'Noise cancelling', 129.99, 'ETH', 2),
                ('Crypto Course', 'Trading course', 199.99, 'SOL', 3),
                ('Code Review', '1-hour review', 79.99, 'BTC', 4)
            ]
            
            for title, desc, price, crypto, cat_id in products_data:
                existing = Product.query.filter_by(title=title).first()
                if not existing:
                    product = Product(
                        title=title,
                        description=desc,
                        price_usd=price,
                        crypto_type=crypto,
                        category_id=cat_id
                    )
                    db.session.add(product)
                    print(f"✅ Created product: {title}")
                else:
                    print(f"⚠️ Product exists: {title}")
            
            db.session.commit()
            print("✅ Products committed")
            
            # Create wallet
            wallet = Wallet(crypto_type='BTC', address='bc1qtestaddress123')
            db.session.add(wallet)
            db.session.commit()
            print("✅ Wallet created")
            
            print("\n🎉 FORCE CLEAN COMPLETE!")
            print("🔑 Login: corner / cornerdooradmin4life")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()
            db.session.rollback()

if __name__ == '__main__':
    force_clean()