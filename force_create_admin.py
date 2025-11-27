import sqlite3
from werkzeug.security import generate_password_hash

def force_create_admin():
    print("FORCE CREATING ADMIN ACCOUNT...")
    print("=" * 50)
    
    # Connect to database
    conn = sqlite3.connect('corner_door.db')
    cursor = conn.cursor()
    
    # Delete any existing user with this username to avoid conflicts
    cursor.execute("DELETE FROM user WHERE username = 'corner'")
    
    # Create the admin account with EXACT credentials
    username = "corner"
    password = "cornerdooradmin4life"
    
    cursor.execute('''
        INSERT INTO user (username, password_hash, is_admin, is_active, recovery_phrase)
        VALUES (?, ?, 1, 1, ?)
    ''', (username, generate_password_hash(password), 'force created admin'))
    
    conn.commit()
    
    # Verify the account was created
    cursor.execute("SELECT username, is_admin, is_active FROM user WHERE username = ?", (username,))
    admin = cursor.fetchone()
    
    if admin:
        print("✅ ADMIN ACCOUNT FORCE-CREATED SUCCESSFULLY!")
        print(f"   Username: {admin[0]}")
        print(f"   Password: {password}")
        print(f"   Is Admin: {bool(admin[1])}")
        print(f"   Is Active: {bool(admin[2])}")
        print("")
        print("🔑 LOGIN CREDENTIALS:")
        print(f"   URL: http://localhost:5000")
        print(f"   Username: {username}")
        print(f"   Password: {password}")
    else:
        print("❌ FAILED to create admin account!")
    
    # Show all admin accounts
    cursor.execute("SELECT username, is_admin, is_active FROM user WHERE is_admin = 1")
    all_admins = cursor.fetchall()
    
    print("")
    print("👥 ALL ADMIN ACCOUNTS IN DATABASE:")
    for admin in all_admins:
        print(f"   - {admin[0]}: Active={admin[2]}, Admin={admin[1]}")
    
    conn.close()

if __name__ == '__main__':
    force_create_admin()