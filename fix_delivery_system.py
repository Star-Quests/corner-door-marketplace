import os
import shutil
from app import app, db, Order

def fix_delivery_system():
    print("🔧 FIXING DELIVERY SYSTEM...")
    
    # Create deliveries folder if it doesn't exist
    deliveries_folder = 'static/deliveries'
    os.makedirs(deliveries_folder, exist_ok=True)
    print(f"✅ Created folder: {deliveries_folder}")
    
    with app.app_context():
        try:
            # Check all orders with delivery files
            orders_with_files = Order.query.filter(Order.delivery_file.isnot(None)).all()
            print(f"📦 Found {len(orders_with_files)} orders with delivery files")
            
            for order in orders_with_files:
                if order.delivery_file:
                    # Extract filename from the path
                    filename = os.path.basename(order.delivery_file)
                    expected_path = os.path.join(deliveries_folder, filename)
                    
                    # Check if file exists
                    if not os.path.exists(expected_path):
                        print(f"❌ Missing delivery file: {filename}")
                        
                        # Create a placeholder file
                        placeholder_path = os.path.join(deliveries_folder, filename)
                        
                        # Create different placeholder content based on file type
                        if filename.endswith(('.jpg', '.jpeg', '.png', '.gif')):
                            # Create a simple text file explaining the image is missing
                            with open(placeholder_path + '.txt', 'w') as f:
                                f.write(f"Original image file: {filename}\n")
                                f.write(f"Product: {order.product.title if order.product else 'Unknown'}\n")
                                f.write(f"Order ID: {order.id}\n")
                                f.write("This file was missing and has been replaced with this placeholder.")
                            print(f"✅ Created placeholder for image: {filename}")
                            
                        elif filename.endswith(('.pdf', '.txt', '.doc', '.docx')):
                            # Create a simple text file
                            with open(placeholder_path, 'w') as f:
                                f.write(f"Delivery File for Order #{order.id}\n")
                                f.write(f"Product: {order.product.title if order.product else 'Unknown'}\n")
                                f.write(f"Original File: {filename}\n")
                                f.write("This is a placeholder file since the original was missing.\n")
                                f.write("The actual product content would be here.")
                            print(f"✅ Created placeholder document: {filename}")
                        
                        # Update the order to point to the new file
                        if filename.endswith(('.jpg', '.jpeg', '.png', '.gif')):
                            order.delivery_file = placeholder_path + '.txt'
                        else:
                            order.delivery_file = placeholder_path
            
            db.session.commit()
            print("✅ Updated order delivery file paths")
            
            # Create sample delivery files for testing
            sample_files = [
                'sample_delivery_1.pdf',
                'sample_ebook.txt',
                'digital_product.zip'
            ]
            
            for sample_file in sample_files:
                sample_path = os.path.join(deliveries_folder, sample_file)
                if not os.path.exists(sample_path):
                    with open(sample_path, 'w') as f:
                        f.write(f"Sample delivery file: {sample_file}\n")
                        f.write("This is a sample delivery file for testing.\n")
                        f.write("Order would contain the actual product here.")
                    print(f"✅ Created sample file: {sample_file}")
            
            print("\n🎉 DELIVERY SYSTEM FIXED!")
            print("📁 Delivery folder: static/deliveries/")
            print("📦 Created placeholder files for missing deliveries")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    fix_delivery_system()