from app import app, db, Order
import os

def check_all_orders():
    print("🔍 CHECKING ALL ORDERS IN DATABASE...")
    
    with app.app_context():
        try:
            orders = Order.query.all()
            print(f"📦 Found {len(orders)} total orders")
            
            for order in orders:
                print(f"\n🔍 Order #{order.id}:")
                print(f"   Product: {order.product.title if order.product else 'Unknown'}")
                print(f"   User: {order.user.username if order.user else 'Unknown'}")
                print(f"   Admin Paid: {order.admin_paid}")
                print(f"   User Paid: {order.user_paid}")
                print(f"   Delivery File: {order.delivery_file}")
                
                if order.delivery_file:
                    if os.path.exists(order.delivery_file):
                        file_size = os.path.getsize(order.delivery_file)
                        print(f"   ✅ File exists ({file_size} bytes)")
                    else:
                        print(f"   ❌ File missing: {order.delivery_file}")
            
            print(f"\n📊 SUMMARY:")
            delivered_orders = [o for o in orders if o.admin_paid]
            orders_with_files = [o for o in delivered_orders if o.delivery_file]
            valid_files = [o for o in orders_with_files if os.path.exists(o.delivery_file)]
            
            print(f"   Total orders: {len(orders)}")
            print(f"   Delivered orders: {len(delivered_orders)}")
            print(f"   Orders with delivery files: {len(orders_with_files)}")
            print(f"   Orders with valid files: {len(valid_files)}")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    check_all_orders()