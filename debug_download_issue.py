from app import app, db
import os

def debug_download_issue():
    print("🐛 DEBUGGING DOWNLOAD ISSUE...")
    
    # Check if there's a static/deliveries folder and what's in it
    deliveries_dir = 'static/deliveries'
    if os.path.exists(deliveries_dir):
        files = os.listdir(deliveries_dir)
        print(f"📁 Files in deliveries folder ({len(files)}):")
        for file in files:
            filepath = os.path.join(deliveries_dir, file)
            file_size = os.path.getsize(filepath)
            print(f"   - {file} ({file_size} bytes)")
    else:
        print("❌ Deliveries folder doesn't exist")
    
    # Check if any file contains "order_4" in the name
    order_4_files = [f for f in files if 'order_4' in f.lower()] if 'files' in locals() else []
    if order_4_files:
        print(f"\n🔍 Found files with 'order_4': {order_4_files}")
    else:
        print(f"\n🔍 No files found with 'order_4' in the name")
    
    print(f"\n💡 The error about Order #4 might be from:")
    print(f"   - A deleted order")
    print(f"   - A direct URL someone tried to access")
    print(f"   - A browser cache issue")
    print(f"   - A previous session")

if __name__ == '__main__':
    debug_download_issue()