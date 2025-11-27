import os
import glob

def complete_reset():
    print("🧹 COMPLETELY RESETTING DATABASE...")
    
    # Delete ALL possible database files
    db_patterns = [
        'corner_door.db',
        'corner_door.db.*',
        'instance/corner_door.db',
        'instance/corner_door.db.*'
    ]
    
    deleted_files = []
    
    for pattern in db_patterns:
        for file_path in glob.glob(pattern):
            try:
                os.remove(file_path)
                deleted_files.append(file_path)
                print(f"✅ Deleted: {file_path}")
            except Exception as e:
                print(f"⚠️  Could not delete {file_path}: {e}")
    
    # Delete instance folder if empty
    try:
        if os.path.exists('instance') and not os.listdir('instance'):
            os.rmdir('instance')
            print("✅ Deleted empty instance folder")
    except:
        pass
    
    if not deleted_files:
        print("ℹ️  No database files found to delete")
    else:
        print(f"✅ Deleted {len(deleted_files)} database files")
    
    print("\n🚀 Now run: python app.py")

if __name__ == '__main__':
    complete_reset()