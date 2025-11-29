def fix_cart_navigation():
    print("🔧 ADDING CART TO NAVIGATION...")
    
    base_template_path = 'templates/base.html'
    
    # Read the current template
    with open(base_template_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Check if cart link exists for regular users
    if 'view_cart' in content:
        # Find where the cart should be placed
        if '{% if current_user.is_admin %}' in content:
            # Add cart link after admin section but before notifications
            old_pattern = '''{% if current_user.is_admin %}
            <a href="{{ url_for('admin_dashboard') }}">Admin</a>
            <a href="{{ url_for('admin_categories') }}">📁 Categories</a>
        {% endif %}'''
            
            new_pattern = '''{% if current_user.is_admin %}
            <a href="{{ url_for('admin_dashboard') }}">Admin</a>
            <a href="{{ url_for('admin_categories') }}">📁 Categories</a>
        {% endif %}
        <a href="{{ url_for('view_cart') }}">🛒 Cart</a>'''
            
            if old_pattern in content and '🛒 Cart' not in content:
                content = content.replace(old_pattern, new_pattern)
                print("✅ Added Cart link to navigation")
        
        # Also check if cart is missing completely
        elif '🛒 Cart' not in content:
            # Add cart link after search
            old_pattern = '''<a href="{{ url_for('search') }}">🔍 Search</a>
        {% if current_user.is_authenticated %}'''
            
            new_pattern = '''<a href="{{ url_for('search') }}">🔍 Search</a>
        {% if current_user.is_authenticated %}
            <a href="{{ url_for('view_cart') }}">🛒 Cart</a>'''
            
            if old_pattern in content:
                content = content.replace(old_pattern, new_pattern)
                print("✅ Added Cart link to navigation")
    
    # Write the updated template
    with open(base_template_path, 'w', encoding='utf-8') as file:
        file.write(content)
    
    print("🎉 CART NAVIGATION FIXED!")
    print("Restart your app to see the changes.")

if __name__ == '__main__':
    fix_cart_navigation()