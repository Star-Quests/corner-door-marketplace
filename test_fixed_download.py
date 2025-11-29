from app import app, db, Order
import os

def test_fixed_download():
    print("🧪 TESTING FIXED DOWNLOAD SYSTEM...")
    
    with app.app_context():
        try:
            # Test order 2 specifically
            order = Order.query.get(2)
            if order:
                print(f"🔍 Order #{order.id}:")
                print(f"   Delivery File: {order.delivery_file}")
                
                if order.delivery_file and os.path.exists(order.delivery_file):
                    print("   ✅ File exists and is accessible")
                    print("   🚀 You can now test the download at: http://localhost:5000/download-delivery/2")
                else:
                    print("   ❌ File still missing")
            else:
                print("❌ Order #2 not found")
                
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == '__main__':
    test_fixed_download()