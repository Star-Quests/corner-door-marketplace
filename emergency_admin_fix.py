import sqlite3
from werkzeug.security import generate_password_hash

def emergency_admin_fix():
    print("EMERGENCY ADMIN ACCOUNT RECOVERY")
    print("=" * 40)
    
    # Connect to database
    conn = sqlite3.connect('corner_door.db')
    cursor = conn.cursor()
    
    # Check current admin status
    cursor.execute("SELECT username, is_active, is_admin FROM user WHERE is_admin = 1")
    admins = cursor.fetchall()
    
    print("Current admin accounts:")
    for admin in admins:
        print(f"  - {admin[0]}: Active={admin[1]}, Admin={admin[2]}")
    
    # Option 1: Reactivate existing admin
    if admins:
        print("\nOption 1: Reactivating existing admin accounts...")
        cursor.execute("UPDATE user SET is_active = 1 WHERE is_admin = 1")
        print("All admin accounts have been reactivated!")
    
    # Option 2: Create new admin if none exist
    else:
        print("\nNo admin accounts found. Creating new admin...")
        cursor.execute('''
            INSERT INTO user (username, password_hash, is_admin, is_active, recovery_phrase)
            VALUES (?, ?, 1, 1, ?)
        ''', ('admin', generate_password_hash('admin123'), 'emergency recovery admin'))
        print("New admin created: username='admin', password='admin123'")
    
    # Verify changes
    cursor.execute("SELECT username, is_active, is_admin FROM user WHERE is_admin = 1")
    updated_admins = cursor.fetchall()
    
    print("\nUpdated admin accounts:")
    for admin in updated_admins:
        print(f"  - {admin[0]}: Active={admin[1]}, Admin={admin[2]}")
    
    # Commit changes
    conn.commit()
    conn.close()
    
    print("\n✅ Admin recovery completed!")
    print("You can now login with:")
    print("   Username: admin")
    print("   Password: admin123")

if __name__ == '__main__':
    emergency_admin_fix()