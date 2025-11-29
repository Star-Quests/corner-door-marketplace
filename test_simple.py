from app import app, db, Category, Product

def test_simple():
    print("🧪 SIMPLE RELATIONSHIP TEST...")
    
    with app.app_context():
        try:
            # Test 1: Check if we can access categories
            categories = Category.query.all()
            print(f"✅ Found {len(categories)} categories")
            
            for category in categories:
                print(f"   - {category.name}: {len(category.products)} products")
            
            # Test 2: Check if we can access category from products
            products = Product.query.limit(3).all()
            print(f"✅ Testing {len(products)} products")
            
            for product in products:
                category_name = product.category.name if product.category else "No category"
                print(f"   - {product.title}: {category_name}")
                
            print("🎉 ALL TESTS PASSED!")
            
        except Exception as e:
            print(f"❌ Test failed: {e}")

if __name__ == '__main__':
    test_simple()