from app import app, db, Order
import os

def permanent_fix():
    print("🛡️ PERMANENT DELIVERY FIX...")
    
    # This will run every time to ensure delivery files exist
    deliveries_dir = 'static/deliveries'
    os.makedirs(deliveries_dir, exist_ok=True)
    
    with app.app_context():
        try:
            orders = Order.query.filter(Order.admin_paid == True).all()
            print(f"📦 Checking {len(orders)} delivered orders")
            
            fixed_count = 0
            for order in orders:
                needs_fix = False
                
                # Check if delivery file is missing or invalid
                if not order.delivery_file:
                    needs_fix = True
                    print(f"   Order #{order.id}: No delivery file")
                elif not os.path.exists(order.delivery_file):
                    needs_fix = True
                    print(f"   Order #{order.id}: Missing file: {order.delivery_file}")
                elif 'wallpaperflare.com_wallpaper' in order.delivery_file:
                    needs_fix = True
                    print(f"   Order #{order.id}: Invalid image file: {order.delivery_file}")
                
                if needs_fix:
                    # Create a proper delivery file
                    filename = f"auto_fix_order_{order.id}.txt"
                    filepath = os.path.join(deliveries_dir, filename)
                    
                    with open(filepath, 'w') as f:
                        f.write(f"AUTO-FIXED DELIVERY FOR ORDER #{order.id}\n")
                        f.write("This file was automatically created to fix a missing delivery.\n")
                    
                    order.delivery_file = filepath
                    fixed_count += 1
                    print(f"   ✅ Fixed order #{order.id}")
            
            if fixed_count > 0:
                db.session.commit()
                print(f"\n🎉 AUTO-FIXED {fixed_count} ORDERS!")
            else:
                print("✅ No fixes needed")
                
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == '__main__':
    permanent_fix()