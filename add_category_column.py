import sqlite3
import os

def add_category_column():
    print("🔧 ADDING MISSING CATEGORY_ID COLUMN...")
    
    # Connect to SQLite database
    conn = sqlite3.connect('corner_door.db')
    cursor = conn.cursor()
    
    try:
        # Check if category_id column exists
        cursor.execute("PRAGMA table_info(product)")
        columns = [column[1] for column in cursor.fetchall()]
        print("📊 Current product table columns:", columns)
        
        if 'category_id' not in columns:
            print("➕ Adding category_id column to product table...")
            cursor.execute("ALTER TABLE product ADD COLUMN category_id INTEGER")
            conn.commit()
            print("✅ category_id column added successfully!")
        else:
            print("✅ category_id column already exists!")
            
        # Verify the column was added
        cursor.execute("PRAGMA table_info(product)")
        columns_after = [column[1] for column in cursor.fetchall()]
        print("📊 Updated product table columns:", columns_after)
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        conn.close()
    
    print("🎉 COLUMN ADDED! Now run: python app.py")

if __name__ == '__main__':
    add_category_column()