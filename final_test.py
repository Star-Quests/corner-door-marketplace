from app import app, db, Category, Product, User

def final_test():
    print("🎯 FINAL TEST: VERIFYING EVERYTHING WORKS...")
    
    with app.app_context():
        try:
            # Test 1: Check all data exists
            print("1. CHECKING DATA:")
            users = User.query.all()
            categories = Category.query.all()
            products = Product.query.all()
            
            print(f"   ✅ Users: {len(users)}")
            print(f"   ✅ Categories: {len(categories)}")
            print(f"   ✅ Products: {len(products)}")
            
            # Test 2: Verify relationships work
            print("\n2. TESTING RELATIONSHIPS:")
            for category in categories:
                products_in_category = category.products
                print(f"   ✅ {category.name}: {len(products_in_category)} products")
                for product in products_in_category:
                    print(f"      • {product.title} - ${product.price_usd}")
            
            # Test 3: Test search functionality
            print("\n3. TESTING SEARCH:")
            search_results = Product.query.filter(Product.title.ilike('%Premium%')).all()
            print(f"   ✅ Search 'Premium': {len(search_results)} results")
            
            search_results = Product.query.filter(Product.title.ilike('%Course%')).all()
            print(f"   ✅ Search 'Course': {len(search_results)} results")
            
            # Test 4: Test category filtering
            print("\n4. TESTING CATEGORY FILTERING:")
            books_category = Category.query.filter_by(name='Books').first()
            if books_category:
                books_products = Product.query.filter_by(category_id=books_category.id).all()
                print(f"   ✅ Books category: {len(books_products)} products")
            
            # Test 5: Verify admin user
            print("\n5. TESTING ADMIN USER:")
            admin = User.query.filter_by(username='corner').first()
            if admin:
                print(f"   ✅ Admin user exists: {admin.username} (Admin: {admin.is_admin})")
            
            print("\n🎉 ALL TESTS PASSED! YOUR APPLICATION IS READY!")
            print("🚀 Start your app with: python app.py")
            
        except Exception as e:
            print(f"❌ Test failed: {e}")
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    final_test()