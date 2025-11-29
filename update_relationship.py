from app import app, db

def update_database():
    print("🔄 UPDATING DATABASE WITH RELATIONSHIP...")
    
    with app.app_context():
        try:
            # This will update your database schema
            db.create_all()
            print("✅ Database updated with relationship!")
            
            # Test the relationship
            from app import Category, Product
            categories = Category.query.all()
            products = Product.query.all()
            
            print(f"✅ Found {len(categories)} categories and {len(products)} products")
            
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == '__main__':
    update_database()