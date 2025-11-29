from app import app, db, Order
import os

def test_download_functionality():
    print("🧪 TESTING DOWNLOAD FUNCTIONALITY...")
    
    with app.app_context():
        try:
            # Get orders with delivery files
            orders = Order.query.filter(Order.delivery_file.isnot(None)).all()
            print(f"📦 Found {len(orders)} orders with delivery files")
            
            for order in orders:
                print(f"\n🔍 Order #{order.id}:")
                print(f"   Product: {order.product.title if order.product else 'Unknown'}")
                print(f"   Delivery File: {order.delivery_file}")
                
                # Check if file exists
                if os.path.exists(order.delivery_file):
                    file_size = os.path.getsize(order.delivery_file)
                    print(f"   ✅ File exists ({file_size} bytes)")
                else:
                    print(f"   ❌ File missing!")
                
                # Check order status
                status = []
                if order.user_paid: status.append("User Paid")
                if order.admin_paid: status.append("Admin Paid")
                if order.delivery_file: status.append("Has Delivery")
                
                print(f"   Status: {', '.join(status)}")
            
            print(f"\n🎉 READY FOR TESTING!")
            print("You can now test downloads at: http://localhost:5000/order/1")
            
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == '__main__':
    test_download_functionality()