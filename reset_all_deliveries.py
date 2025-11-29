from app import app, db, Order
import os
from datetime import datetime

def reset_all_deliveries():
    print("🔄 RESETTING ALL DELIVERY FILES...")
    
    # Ensure deliveries directory exists
    deliveries_dir = 'static/deliveries'
    os.makedirs(deliveries_dir, exist_ok=True)
    
    with app.app_context():
        try:
            # Get all orders
            orders = Order.query.all()
            print(f"📦 Processing {len(orders)} orders")
            
            reset_count = 0
            for order in orders:
                if order.admin_paid:  # Only reset delivered orders
                    # Create a proper delivery file name
                    product_name = order.product.title if order.product else f"Product_{order.id}"
                    # Make filename safe
                    safe_name = "".join(c for c in product_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
                    safe_name = safe_name.replace(' ', '_')[:30]  # Limit length
                    filename = f"delivery_order_{order.id}_{safe_name}.txt"
                    filepath = os.path.join(deliveries_dir, filename)
                    
                    # Create the delivery content
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(f"DELIVERY FOR ORDER #{order.id}\n")
                        f.write("=" * 50 + "\n")
                        f.write(f"PRODUCT: {product_name}\n")
                        f.write(f"ORDER DATE: {order.created_at.strftime('%Y-%m-%d %H:%M')}\n")
                        f.write(f"DELIVERY DATE: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
                        f.write(f"AMOUNT: ${order.product.price_usd if order.product else 0:.2f} USD\n")
                        f.write(f"CRYPTO: {order.crypto_amount:.8f} {order.crypto_type}\n")
                        f.write(f"STATUS: {'PAID' if order.user_paid else 'PENDING'}\n")
                        f.write("\n" + "=" * 50 + "\n")
                        f.write("PRODUCT CONTENT:\n\n")
                        f.write("This file contains your purchased digital product.\n")
                        f.write("If this were a real product, you would find:\n")
                        f.write("- Ebook content\n")
                        f.write("- Software license keys\n") 
                        f.write("- Course materials\n")
                        f.write("- Download links\n")
                        f.write("- Or other digital content\n")
                        f.write("\n" + "=" * 50 + "\n")
                        f.write("Thank you for your purchase!\n")
                        f.write("CORNER DOOR MARKETPLACE\n")
                    
                    # Update the order with the new file path
                    order.delivery_file = filepath
                    reset_count += 1
                    print(f"✅ Reset order #{order.id}: {filename}")
            
            if reset_count > 0:
                db.session.commit()
                print(f"\n🎉 RESET {reset_count} DELIVERY FILES!")
            else:
                print("✅ No orders needed reset")
            
            # Show all delivery files
            print(f"\n📄 DELIVERY FILES IN FOLDER:")
            if os.path.exists(deliveries_dir):
                files = os.listdir(deliveries_dir)
                for file in files:
                    full_path = os.path.join(deliveries_dir, file)
                    file_size = os.path.getsize(full_path)
                    print(f"   - {file} ({file_size} bytes)")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()
            db.session.rollback()

if __name__ == '__main__':
    reset_all_deliveries()