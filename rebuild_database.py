import os
from app import app, db
from werkzeug.security import generate_password_hash

def rebuild_database():
    print("🏗️ REBUILDING DATABASE FROM SCRATCH...")
    
    # Remove existing database files
    db_files = ['corner_door.db', 'corner_door.db-wal', 'corner_door.db-shm']
    for db_file in db_files:
        if os.path.exists(db_file):
            os.remove(db_file)
            print(f"✅ Removed: {db_file}")
    
    with app.app_context():
        try:
            # Create all tables
            db.create_all()
            print("✅ All database tables created!")
            
            # Import models after db.create_all()
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
            
            # Create categories
            categories = [
                Category(name='Books', description='Digital and physical books'),
                Category(name='Electronics', description='Gadgets and electronic devices'),
                Category(name='Digital Products', description='Software, courses, and digital content'),
                Category(name='Services', description='Consultations and various services')
            ]
            for category in categories:
                db.session.add(category)
            db.session.commit()
            print("✅ Categories created")
            
            # Create sample products with categories
            products = [
                Product(
                    title='Premium Ebook Bundle',
                    description='Collection of premium ebooks on various topics',
                    price_usd=49.99,
                    crypto_type='BTC',
                    admin_rating=5,
                    category_id=1  # Books
                ),
                Product(
                    title='Wireless Headphones',
                    description='High-quality wireless headphones with noise cancellation',
                    price_usd=129.99,
                    crypto_type='ETH',
                    admin_rating=4,
                    category_id=2  # Electronics
                ),
                Product(
                    title='Cryptocurrency Course',
                    description='Complete course on cryptocurrency trading and investment',
                    price_usd=199.99,
                    crypto_type='SOL',
                    admin_rating=5,
                    category_id=3  # Digital Products
                ),
                Product(
                    title='Programming Consultation',
                    description='One-hour programming consultation session',
                    price_usd=79.99,
                    crypto_type='BTC',
                    admin_rating=5,
                    category_id=4  # Services
                )
            ]
            for product in products:
                db.session.add(product)
            db.session.commit()
            print("✅ Sample products created with categories")
            
            # Create wallet
            wallet = Wallet(
                crypto_type='BTC',
                address='bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh'
            )
            db.session.add(wallet)
            db.session.commit()
            print("✅ Wallet address added")
            
            print("\n🎉 DATABASE REBUILD COMPLETE!")
            print("🔑 Admin Login: corner / cornerdooradmin4life")
            print("📊 Includes: 4 categories, 4 sample products, wallet address")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    rebuild_database()