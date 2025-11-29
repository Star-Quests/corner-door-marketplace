# Fix Delivery File Paths PowerShell Script
Write-Host "🔧 FIXING DELIVERY FILE PATHS..." -ForegroundColor Green

# Start Python and run the fix
python -c "
import os
from app import app, db, Order

with app.app_context():
    orders = Order.query.filter(Order.delivery_file.isnot(None)).all()
    print(f'📦 Found {len(orders)} orders with delivery files')
    
    for order in orders:
        if order.delivery_file:
            old_path = order.delivery_file
            # Fix backslashes and ensure correct path
            new_path = old_path.replace('\\\\', '/')
            if not new_path.startswith('static/'):
                filename = new_path.split('\\\\')[-1]  # Get filename
                new_path = f'static/deliveries/{filename}'
            
            order.delivery_file = new_path
            print(f'✅ Fixed order #{order.id}: {new_path}')
    
    db.session.commit()
    print('🎉 ALL PATHS FIXED!')
"

Write-Host "🎉 DELIVERY PATHS FIXED!" -ForegroundColor Green
