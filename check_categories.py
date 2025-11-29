from app import app, db, Category, Product

with app.app_context():
    # Check if categories table exists and has columns
    try:
        categories = Category.query.all()
        print(f"✅ Categories table exists with {len(categories)} categories")
        
        # Check if products have category_id column
        products_with_categories = Product.query.filter(Product.category_id.isnot(None)).count()
        print(f"✅ {products_with_categories} products have categories assigned")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Creating database tables...")
        db.create_all()
        print("✅ Database tables created successfully!")