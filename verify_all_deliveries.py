from app import app, db, Order
import os

def verify_all_deliveries():
    print("🔍 VERIFYING ALL DELIVERY FILES...")
    
    with app.app_context():
        try:
            orders = Order.query.all()
            print(f"📦 Checking {len(orders)} orders")
            
            valid_count = 0
            missing_count = 0
            
            for order in orders:
                print(f"\n🔍 Order #{order.id}:")
                print(f"   Product: {order.product.title if order.product else 'Unknown'}")
                print(f"   Delivery File: {order.delivery_file}")
                
                if order.delivery_file:
                    if os.path.exists(order.delivery_file):
                        file_size = os.path.getsize(order.delivery_file)
                        print(f"   ✅ VALID ({file_size} bytes)")
                        valid_count += 1
                    else:
                        print(f"   ❌ MISSING")
                        missing_count += 1
                else:
                    print(f"   ⚠️  NO DELIVERY FILE")
                    missing_count += 1
            
            print(f"\n📊 SUMMARY:")
            print(f"   ✅ Valid delivery files: {valid_count}")
            print(f"   ❌ Missing delivery files: {missing_count}")
            print(f"   📦 Total orders: {len(orders)}")
            
            if missing_count == 0:
                print("🎉 ALL DELIVERY FILES ARE VALID!")
                print("🚀 You can now test downloads for all orders")
            else:
                print("❌ Some delivery files are still missing")
                
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == '__main__':
    verify_all_deliveries()