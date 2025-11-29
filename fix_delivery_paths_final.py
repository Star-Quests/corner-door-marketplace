import os
from app import app, db, Order

def fix_delivery_paths():
    print("🔧 FIXING DELIVERY FILE PATHS FINAL...")
    
    with app.app_context():
        try:
            orders = Order.query.filter(Order.delivery_file.isnot(None)).all()
            print(f"📦 Found {len(orders)} orders with delivery files")
            
            for order in orders:
                if order.delivery_file:
                    # Fix backslashes to forward slashes
                    old_path = order.delivery_file
                    new_path = old_path.replace('\\', '/')
                    
                    if old_path != new_path:
                        order.delivery_file = new_path
                        print(f"✅ Fixed path for order #{order.id}: {new_path}")
            
            db.session.commit()
            print("🎉 DELIVERY PATHS FIXED!")
            
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == '__main__':
    fix_delivery_paths()