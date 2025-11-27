import sqlite3

def fix_admin_account():
    # Connect to the database
    conn = sqlite3.connect('corner_door.db')
    cursor = conn.cursor()
    
    # Reactivate the admin account
    cursor.execute("UPDATE user SET is_active = 1 WHERE username = 'admin'")
    
    # Commit changes
    conn.commit()
    
    # Verify the change
    cursor.execute("SELECT username, is_active, is_admin FROM user WHERE username = 'admin'")
    admin = cursor.fetchone()
    
    if admin:
        print(f"Admin account fixed: {admin}")
    else:
        print("Admin account not found!")
    
    conn.close()

if __name__ == '__main__':
    fix_admin_account()
    print("Run: python fix_admin.py to reactivate your admin account")