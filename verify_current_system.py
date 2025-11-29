from app import app, db, Order
import os

def verify_current_system():
    print("✅ VERIFYING CURRENT SYSTEM STATUS...")
    
    with app.app_context():
        orders = Order.query.all()
        
        if not orders:
            print("❌ No orders found in database")
            return
        
        print(f"📦 Found {len(orders)} orders")
        print("\n🧪 Testing download readiness:")
        
        for order in orders:
            if order.admin_paid and order.delivery_file and os.path.exists(order.delivery_file):
                print(f"   ✅ Order #{order.id}: READY for download")
                print(f"      URL: http://localhost:5000/download-delivery/{order.id}")
            else:
                status = []
                if not order.admin_paid: status.append("Not delivered")
                if not order.delivery_file: status.append("No delivery file")
                if order.delivery_file and not os.path.exists(order.delivery_file): status.append("File missing")
                print(f"   ❌ Order #{order.id}: {', '.join(status)}")
        
        print(f"\n🎯 INSTRUCTIONS:")
        print(f"   1. Test working orders at the URLs above")
        print(f"   2. For broken orders, login as admin and re-deliver")
        print(f"   3. The system will now handle missing files automatically")

if __name__ == '__main__':
    verify_current_system()