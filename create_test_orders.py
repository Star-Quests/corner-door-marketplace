from app import app, db, User, Product, Order
from werkzeug.security import generate_password_hash
import os
from datetime import datetime, timedelta

def create_test_orders():
    print("📦 CREATING TEST ORDERS WITH DELIVERIES...")
    
    with app.app_context():
        try:
            # Create test user if doesn't exist
            test_user = User.query.filter_by(username='testuser').first()
            if not test_user:
                test_user = User(
                    username='testuser',
                    password_hash=generate_password_hash('test123'),
                    is_active=True
                )
                db.session.add(test_user)
                print("✅ Created test user: testuser / test123")
            
            # Get or create products
            products = Product.query.all()
            if not products:
                print("❌ No products found. Creating sample products...")
                products = [
                    Product(title='Premium Ebook', description='Digital ebook', price_usd=29.99, crypto_type='BTC'),
                    Product(title='Software License', description='Software product', price_usd=99.99, crypto_type='ETH'),
                    Product(title='Online Course', description='Video course', price_usd=149.99, crypto_type='SOL')
                ]
                for product in products:
                    db.session.add(product)
            
            # Create delivery files directory
            deliveries_dir = 'static/deliveries'
            os.makedirs(deliveries_dir, exist_ok=True)
            
            # Create sample delivery files
            delivery_files = {
                'ebook_delivery.pdf': """
                PREMIUM EBOOK - ORDER #001
                ==========================
                
                Thank you for purchasing our Premium Ebook!
                
                This ebook includes:
                - 10 chapters of expert content
                - Practical examples and exercises
                - Lifetime updates
                
                File: ebook_delivery.pdf
                Order Date: {date}
                
                Enjoy your reading!
                """,
                
                'software_license.txt': """
                SOFTWARE LICENSE - ORDER #002
                ============================
                
                License Information:
                Product: Professional Software Suite
                License Key: LICENSE-{date}-ABC123
                Version: 2.0
                Valid Until: 2026-12-31
                
                Installation:
                1. Download from our website
                2. Enter the license key above
                3. Complete activation
                
                Support: support@example.com
                """,
                
                'course_access.zip': """
                ONLINE COURSE ACCESS - ORDER #003
                ================================
                
                Welcome to our Online Course!
                
                Course Materials Included:
                - Video Lessons (12 hours)
                - PDF Study Guides
                - Exercise Files
                - Certificate of Completion
                
                Access Instructions:
                1. Extract this ZIP file
                2. Follow the setup guide
                3. Start learning!
                
                Order Date: {date}
                """
            }
            
            # Create the delivery files
            for filename, content in delivery_files.items():
                filepath = os.path.join(deliveries_dir, filename)
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content.format(date=datetime.now().strftime('%Y-%m-%d')))
                print(f"✅ Created delivery file: {filename}")
            
            # Create test orders
            test_orders = []
            for i, product in enumerate(products[:3]):  # Use first 3 products
                delivery_filename = list(delivery_files.keys())[i]
                delivery_filepath = os.path.join(deliveries_dir, delivery_filename)
                
                order = Order(
                    user_id=test_user.id,
                    product_id=product.id,
                    crypto_type=product.crypto_type,
                    wallet_address='test_wallet_address_123',
                    crypto_amount=product.price_usd / 50000,  # Rough conversion
                    user_paid=True,
                    admin_paid=True,
                    delivery_location='Digital delivery via download',
                    delivery_file=delivery_filepath,
                    delivery_notes=f'Automated test delivery for {product.title}',
                    created_at=datetime.now() - timedelta(days=i)
                )
                test_orders.append(order)
                db.session.add(order)
                print(f"✅ Created test order #{i+1} for: {product.title}")
            
            db.session.commit()
            
            print(f"\n🎉 CREATED {len(test_orders)} TEST ORDERS!")
            print("📦 Orders are marked as paid and delivered")
            print("📁 Delivery files created in: static/deliveries/")
            print("👤 Test user: testuser / test123")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()
            db.session.rollback()

if __name__ == '__main__':
    create_test_orders()