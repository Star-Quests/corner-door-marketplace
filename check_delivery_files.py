from app import app, db, Order
import os

def check_delivery_files():
    print("🔍 CHECKING DELIVERY FILES IN DATABASE...")
    
    with app.app_context():
        try:
            orders = Order.query.all()
            print(f"📦 Found {len(orders)} total orders")
            
            for order in orders:
                print(f"\n🔍 Order #{order.id}:")
                print(f"   Product: {order.product.title if order.product else 'Unknown'}")
                print(f"   Delivery File: {order.delivery_file}")
                print(f"   Admin Paid: {order.admin_paid}")
                print(f"   User Paid: {order.user_paid}")
                
                if order.delivery_file:
                    if os.path.exists(order.delivery_file):
                        file_size = os.path.getsize(order.delivery_file)
                        print(f"   ✅ File exists ({file_size} bytes)")
                    else:
                        print(f"   ❌ File missing: {order.delivery_file}")
                        
                        # Show what's actually in the deliveries folder
                        deliveries_dir = 'static/deliveries'
                        if os.path.exists(deliveries_dir):
                            files = os.listdir(deliveries_dir)
                            print(f"   📁 Files in deliveries folder: {files}")
            
            print(f"\n📊 Summary:")
            orders_with_files = [o for o in orders if o.delivery_file]
            orders_with_valid_files = [o for o in orders_with_files if os.path.exists(o.delivery_file)]
            print(f"   Orders with delivery files: {len(orders_with_files)}")
            print(f"   Orders with valid files: {len(orders_with_valid_files)}")
            
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == '__main__':
    check_delivery_files()