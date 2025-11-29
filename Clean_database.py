import os
import sqlite3
from app import app, db
from werkzeug.security import generate_password_hash

def clean_database():
    print("🧹 COMPLETE DATABASE CLEANUP...")
    
    # Remove all database files completely
    db_files = ['corner_door.db', 'corner_door.db-wal', 'corner_door.db-shm']
    for db_file in db_files:
        if os.path.exists(db_file):
            os.remove(db_file)
            print(f"✅ Removed: {db_file}")
    
    # Also check for instance folder
    instance_db = 'instance/corner_door.db'
    if os.path.exists(instance_db):
        os.remove(instance_db)
        print(f"✅ Removed: {instance_db}")
    
    with app.app_context():
        try:
            # Create all tables from scratch
            db.create_all()
            print("✅ All database tables created!")
            
            # Now import models and create data
            from app import User, Category, Product, Wallet
            
            # Create admin user
            admin = User(
                username='corner',
                password_hash=generate_password_hash('cornerdooradmin4life'),
                is_admin=True,
                is_active=True,
                recovery_phrase='primary admin account'
            )
            db.session.add(admin)
            print("✅ Admin user created")
            
            # Commit admin first
            db.session.commit()
            
            # Now create categories one by one with error handling
            print("📁 Creating categories...")
            category_data = [
                ('Books', 'Digital and physical books'),
                ('Electronics', 'Gadgets and electronic devices'),
                ('Digital Products', 'Software, courses, and digital content'),
                ('Services', 'Consultations and various services')
            ]
            
            for name, description in category_data:
                try:
                    # Check if category already exists
                    existing = Category.query.filter_by(name=name).first()
                    if not existing:
                        category = Category(name=name, description=description)
                        db.session.add(category)
                        print(f"✅ Created category: {name}")
                    else:
                        print(f"⚠️ Category already exists: {name}")
                except Exception as e:
                    print(f"❌ Error creating category {name}: {e}")
            
            db.session.commit()
            print("✅ Categories processed")
            
            # Create sample products
            print("📦 Creating sample products...")
            products_data = [
                ('Premium Ebook Bundle', 'Collection of premium ebooks', 49.99, 'BTC', 1),
                ('Wireless Headphones', 'Noise cancelling headphones', 129.99, 'ETH', 2),
                ('Crypto Trading Course', 'Complete trading course', 199.99, 'SOL', 3),
                ('Programming Consultation', '1-hour coding help', 79.99, 'BTC', 4)
            ]
            
            for title, description, price, crypto, category_id in products_data:
                try:
                    product = Product(
                        title=title,
                        description=description,
                        price_usd=price,
                        crypto_type=crypto,
                        admin_rating=5,
                        category_id=category_id
                    )
                    db.session.add(product)
                    print(f"✅ Created product: {title}")
                except Exception as e:
                    print(f"❌ Error creating product {title}: {e}")
            
            db.session.commit()
            print("✅ Products created")
            
            # Create wallet
            wallet = Wallet(
                crypto_type='BTC',
                address='bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh'
            )
            db.session.add(wallet)
            db.session.commit()
            print("✅ Wallet created")
            
            print("\n🎉 DATABASE SETUP COMPLETE!")
            print("🔑 Admin: corner / cornerdooradmin4life")
            
        except Exception as e:
            print(f"❌ Error during setup: {e}")
            import traceback
            traceback.print_exc()
            db.session.rollback()

if __name__ == '__main__':
    clean_database()