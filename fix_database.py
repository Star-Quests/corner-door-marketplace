from app import app, db, Product
import sqlite3
import os

def fix_database():
    print("🔧 FIXING DATABASE...")
    
    with app.app_context():
        try:
            # Check if category_id column exists
            conn = sqlite3.connect('corner_door.db')
            cursor = conn.cursor()
            
            # Get table info
            cursor.execute("PRAGMA table_info(product)")
            columns = [column[1] for column in cursor.fetchall()]
            
            if 'category_id' not in columns:
                print("➕ Adding category_id column to product table...")
                cursor.execute("ALTER TABLE product ADD COLUMN category_id INTEGER")
                conn.commit()
                print("✅ category_id column added successfully!")
            else:
                print("✅ category_id column already exists!")
            
            conn.close()
            
            # Verify the fix
            products = Product.query.all()
            print(f"✅ Database fixed! Found {len(products)} products")
            
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == '__main__':
    fix_database()