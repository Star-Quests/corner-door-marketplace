import sqlite3

def verify_fix():
    print("🔍 VERIFYING DATABASE FIX...")
    
    conn = sqlite3.connect('corner_door.db')
    cursor = conn.cursor()
    
    try:
        # Check product table structure
        cursor.execute("PRAGMA table_info(product)")
        product_columns = cursor.fetchall()
        print("📊 PRODUCT TABLE COLUMNS:")
        for col in product_columns:
            print(f"   - {col[1]} ({col[2]})")
        
        # Check category table structure
        cursor.execute("PRAGMA table_info(category)")
        category_columns = cursor.fetchall()
        print("📊 CATEGORY TABLE COLUMNS:")
        for col in category_columns:
            print(f"   - {col[1]} ({col[2]})")
        
        # Check if we have data
        cursor.execute("SELECT COUNT(*) FROM product")
        product_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM category")
        category_count = cursor.fetchone()[0]
        
        print(f"📈 DATA COUNTS: {product_count} products, {category_count} categories")
        
        # Test a simple query
        cursor.execute("SELECT id, title, category_id FROM product LIMIT 3")
        sample_products = cursor.fetchall()
        print("🔍 SAMPLE PRODUCTS:")
        for product in sample_products:
            print(f"   - ID: {product[0]}, Title: {product[1]}, Category ID: {product[2]}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        conn.close()

if __name__ == '__main__':
    verify_fix()