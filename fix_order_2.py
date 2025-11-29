from app import app, db, Order
import os

def fix_order_2():
    print("🔧 FIXING ORDER #2 DELIVERY FILE...")
    
    with app.app_context():
        try:
            # Get order 2
            order = Order.query.get(2)
            if not order:
                print("❌ Order #2 not found")
                return
            
            print(f"📦 Order #{order.id}: {order.product.title if order.product else 'Unknown'}")
            print(f"📁 Current delivery file: {order.delivery_file}")
            
            # Check what delivery files exist
            deliveries_dir = 'static/deliveries'
            if os.path.exists(deliveries_dir):
                existing_files = os.listdir(deliveries_dir)
                print(f"📄 Existing delivery files: {existing_files}")
                
                if existing_files:
                    # Use the first available file
                    new_file = os.path.join(deliveries_dir, existing_files[0])
                    order.delivery_file = new_file
                    db.session.commit()
                    print(f"✅ Updated order #{order.id} to use: {new_file}")
                else:
                    print("❌ No delivery files found. Creating one...")
                    # Create a delivery file
                    filepath = os.path.join(deliveries_dir, 'fixed_delivery_2.txt')
                    with open(filepath, 'w') as f:
                        f.write(f"Delivery for Order #{order.id}\n")
                        f.write(f"Product: {order.product.title if order.product else 'Unknown'}\n")
                        f.write("This file was created to fix the missing delivery issue.\n")
                    
                    order.delivery_file = filepath
                    db.session.commit()
                    print(f"✅ Created and assigned: {filepath}")
            else:
                print("❌ Deliveries folder doesn't exist")
                
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    fix_order_2()