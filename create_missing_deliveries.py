import os
from app import app, db, Order

def create_missing_deliveries():
    print("📦 CREATING MISSING DELIVERY FILES...")
    
    with app.app_context():
        try:
            orders = Order.query.filter(Order.delivery_file.isnot(None)).all()
            
            for order in orders:
                if order.delivery_file and not os.path.exists(order.delivery_file):
                    # Create the missing file
                    filename = os.path.basename(order.delivery_file)
                    
                    with open(order.delivery_file, 'w') as f:
                        f.write(f"DELIVERY FILE FOR ORDER #{order.id}\n")
                        f.write(f"Product: {order.product.title if order.product else 'Unknown'}\n")
                        f.write(f"Order Date: {order.created_at}\n")
                        f.write("\nThank you for your purchase!\n")
                        f.write("This is your digital product delivery.\n")
                    
                    print(f"✅ Created missing file: {filename}")
            
            print("🎉 MISSING DELIVERY FILES CREATED!")
            
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == '__main__':
    create_missing_deliveries()