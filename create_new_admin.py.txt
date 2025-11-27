import sqlite3
from werkzeug.security import generate_password_hash

def create_new_admin():
    print("CREATING NEW ADMIN ACCOUNT...")
    print("=" * 40)
    
    # Connect to database
    conn = sqlite3.connect('corner_door.db')
    cursor = conn.cursor()
    
    # Get username and password from user
    username = input("Enter new admin username: ").strip()
    password = input("Enter new admin password: ").strip()
    
    if not username or not password:
        print("❌ Username and password cannot be empty!")
        return
    
    # Check if username already exists
    cursor.execute("SELECT username FROM user WHERE username = ?", (username,))
    if cursor.fetchone():
        print(f"❌ Username '{username}' already exists!")
        conn.close()
        return
    
    # Create new admin user
    cursor.execute('''
        INSERT INTO user (username, password_hash, is_admin, is_active, recovery_phrase)
        VALUES (?, ?, 1, 1, ?)
    ''', (username, generate_password_hash(password), 'admin recovery account'))
    
    conn.commit()
    
    # Verify the new admin
    cursor.execute("SELECT username, is_admin, is_active FROM user WHERE username = ?", (username,))
    admin = cursor.fetchone()
    
    if admin:
        print("✅ NEW ADMIN ACCOUNT CREATED SUCCESSFULLY!")
        print(f"   Username: {admin[0]}")
        print(f"   Password: {password}")
        print(f"   Is Admin: {bool(admin[1])}")
        print(f"   Is Active: {bool(admin[2])}")
    else:
        print("❌ Failed to create admin account!")
    
    conn.close()

if __name__ == '__main__':
    create_new_admin()