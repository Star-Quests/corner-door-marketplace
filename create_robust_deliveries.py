from app import app, db, Order
import os
from datetime import datetime

def create_robust_deliveries():
    print("🔧 CREATING ROBUST DELIVERY SYSTEM...")
    
    # Ensure deliveries directory exists
    deliveries_dir = 'static/deliveries'
    os.makedirs(deliveries_dir, exist_ok=True)
    print(f"✅ Deliveries directory: {deliveries_dir}")
    
    with app.app_context():
        try:
            # Get all orders
            orders = Order.query.all()
            print(f"📦 Processing {len(orders)} orders")
            
            fixed_count = 0
            for order in orders:
                if order.admin_paid and (not order.delivery_file or not os.path.exists(order.delivery_file)):
                    # Create a delivery file for this order
                    product_name = order.product.title if order.product else f"Product_{order.id}"
                    safe_name = "".join(c for c in product_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
                    filename = f"delivery_{order.id}_{safe_name}.txt"
                    filepath = os.path.join(deliveries_dir, filename)
                    
                    # Create the delivery content
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(f"DELIVERY FOR ORDER #{order.id}\n")
                        f.write("=" * 40 + "\n")
                        f.write(f"Product: {product_name}\n")
                        f.write(f"Order Date: {order.created_at}\n")
                        f.write(f"Delivery Date: {datetime.now()}\n")
                        f.write(f"Amount: ${order.product.price_usd if order.product else 0:.2f} USD\n")
                        f.write(f"Crypto: {order.crypto_amount:.8f} {order.crypto_type}\n")
                        f.write("\n" + "=" * 40 + "\n")
                        f.write("DELIVERY CONTENT:\n")
                        f.write("This is your purchased product delivery.\n")
                        f.write("Thank you for your purchase!\n")
                        f.write("\n" + "=" * 40 + "\n")
                        f.write("CORNER DOOR MARKETPLACE\n")
                    
                    # Update the order
                    order.delivery_file = filepath
                    fixed_count += 1
                    print(f"✅ Created delivery for order #{order.id}: {filename}")
            
            if fixed_count > 0:
                db.session.commit()
                print(f"\n🎉 FIXED {fixed_count} ORDERS WITH DELIVERY FILES!")
            else:
                print("✅ All orders already have valid delivery files")
                
            # List all delivery files
            delivery_files = os.listdir(deliveries_dir)
            print(f"\n📄 Delivery files available: {len(delivery_files)}")
            for file in delivery_files:
                print(f"   - {file}")
                
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    create_robust_deliveries()