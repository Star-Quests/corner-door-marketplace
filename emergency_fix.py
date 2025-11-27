import sqlite3
from werkzeug.security import generate_password_hash

def emergency_admin_recovery():
    print("🚨 EMERGENCY ADMIN RECOVERY")
    print("=" * 50)
    
    # Connect to your existing database
    conn = sqlite3.connect('corner_door.db')
    cursor = conn.cursor()
    
    # Check what admin accounts exist
    cursor.execute("SELECT username, is_active, is_admin FROM user WHERE is_admin = 1")
    admins = cursor.fetchall()
    
    print("Current admin accounts found:")
    for admin in admins:
        print(f"  - {admin[0]}: Active={admin[1]}, Admin={admin[2]}")
    
    # OPTION 1: Reactivate existing admin
    if admins:
        print("\n🔄 Reactivating all admin accounts...")
        cursor.execute("UPDATE user SET is_active = 1 WHERE is_admin = 1")
        print("✅ All admin accounts reactivated!")
    
    # OPTION 2: Create new admin if none exist
    else:
        print("\n👤 No admin accounts found. Creating new ones...")
        # Create main admin
        cursor.execute(
            "INSERT INTO user (username, password_hash, is_admin, is_active) VALUES (?, ?, ?, ?)",
            ('admin', generate_password_hash('admin123'), 1, 1)
        )
        # Create backup admin
        cursor.execute(
            "INSERT INTO user (username, password_hash, is_admin, is_active) VALUES (?, ?, ?, ?)",
            ('superadmin', generate_password_hash('superadmin123'), 1, 1)
        )
        print("✅ New admin accounts created!")
    
    # Verify the fix
    cursor.execute("SELECT username, is_active, is_admin FROM user WHERE is_admin = 1")
    updated_admins = cursor.fetchall()
    
    print("\n✅ RECOVERY COMPLETE!")
    print("Updated admin accounts:")
    for admin in updated_admins:
        print(f"  - {admin[0]}: Active={admin[1]}")
    
    print("\n🎯 LOGIN CREDENTIALS:")
    print("   👤 Username: admin")
    print("   🔑 Password: admin123")
    print("   👤 Backup: superadmin")
    print("   🔑 Backup Password: superadmin123")
    
    conn.commit()
    conn.close()

if __name__ == '__main__':
    emergency_admin_recovery()