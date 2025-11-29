from app import app, db
import os

def fix_relationship():
    print("🔧 FIXING RELATIONSHIP CONFLICT...")
    
    # Delete the database to start fresh
    if os.path.exists('corner_door.db'):
        os.remove('corner_door.db')
        print("✅ Old database deleted")
    
    with app.app_context():
        try:
            # Create all tables with corrected relationships
            db.create_all()
            print("✅ Database created with fixed relationships!")
            
            # Add test data
            from app import Category, Product, User
            from werkzeug.security import generate_password_hash
            
            # Create admin
            admin = User(
                username='corner',
                password_hash=generate_password_hash('cornerdooradmin4life'),
                is_admin=True,
                is_active=True,
                recovery_phrase='primary admin'
            )
            db.session.add(admin)
            
            # Create categories
            categories = [
                Category(name='Books', description='Digital and physical books'),
                Category(name='Electronics', description='Gadgets and devices'),
                Category(name='Digital Products', description='Software and courses')
            ]
            for category in categories:
                db.session.add(category)
            
            db.session.commit()
            print("✅ Categories created!")
            
            # Test the relationship
            books_category = Category.query.filter_by(name='Books').first()
            print(f"✅ Relationship test: Category '{books_category.name}' has {len(books_category.products)} products")
            
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == '__main__':
    fix_relationship()