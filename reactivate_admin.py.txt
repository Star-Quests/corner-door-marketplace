import sqlite3
from werkzeug.security import generate_password_hash

def reactivate_admin():
    print("🔧 REACTIVATING ADMIN ACCOUNT...")
    
    # Connect to database
    conn = sqlite3.connect('corner_door.db')
    cursor = conn.cursor()
    
    # Check current admin status
    cursor.execute("SELECT username, is_active, is_admin FROM user WHERE username = 'admin'")
    admin = cursor.fetchone()
    
    if admin:
        print(f"Current admin status: {admin}")
        
        # Reactivate admin account
        cursor.execute("UPDATE user SET is_active = 1 WHERE username = 'admin'")
        print("✅ Admin account reactivated!")
    else:
        # Create new admin account
        print("❌ Admin account not found. Creating new one...")
        cursor.execute('''
            INSERT INTO user (username, password_hash, is_admin, is_active, recovery_phrase)
            VALUES (?, ?, 1, 1, ?)
        ''', ('admin', generate_password_hash('admin123'), 'emergency recovery admin'))
        print("✅ New admin account created!")
    
    # Verify the change
    cursor.execute("SELECT username, is_active, is_admin FROM user WHERE username = 'admin'")
    updated_admin = cursor.fetchone()
    print(f"✅ Updated admin status: {updated_admin}")
    
    # Commit changes
    conn.commit()
    conn.close()
    
    print("\n🎉 ADMIN ACCOUNT RECOVERY COMPLETE!")
    print("You can now login with:")
    print("   👤 Username: admin")
    print("   🔑 Password: admin123")

if __name__ == '__main__':
    reactivate_admin()