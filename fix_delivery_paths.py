import os
from app import app, db, Order

def fix_delivery_paths():
    print("🔧 FIXING DELIVERY FILE PATHS...")
    
    with app.app_context():
        try:
            # Create deliveries directory
            deliveries_dir = 'static/deliveries'
            os.makedirs(deliveries_dir, exist_ok=True)
            print(f"✅ Created directory: {deliveries_dir}")
            
            # Fix all orders with delivery files
            orders = Order.query.filter(Order.delivery_file.isnot(None)).all()
            print(f"📦 Found {len(orders)} orders with delivery files")
            
            for order in orders:
                if order.delivery_file:
                    # Fix the path format
                    old_path = order.delivery_file
                    
                    # Convert backslashes to forward slashes and fix path
                    if 'static/deliveries' in old_path:
                        # Extract just the filename
                        filename = os.path.basename(old_path)
                        new_path = f"static/deliveries/{filename}"
                        
                        # Update the order with correct path
                        order.delivery_file = new_path
                        print(f"✅ Fixed path for order #{order.id}: {filename}")
            
            db.session.commit()
            print("🎉 DELIVERY PATHS FIXED!")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    fix_delivery_paths()