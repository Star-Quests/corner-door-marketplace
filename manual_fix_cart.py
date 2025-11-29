import os

def manual_fix():
    print("🔧 MANUAL CART FIX...")
    
    # Try different template locations
    template_locations = [
        'templates/base.html',
        'templates/base.html.txt', 
        'base.html',
        'base.html.txt'
    ]
    
    template_path = None
    for location in template_locations:
        if os.path.exists(location):
            template_path = location
            print(f"✅ Found template at: {template_path}")
            break
    
    if not template_path:
        print("❌ No template file found. Please check your project structure.")
        return
    
    # Read the template
    with open(template_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Check if cart link already exists
    if '🛒 Cart' in content or 'view_cart' in content:
        print("✅ Cart link already exists in navigation")
        return
    
    # Add cart link to navigation
    if '{% if current_user.is_admin %}' in content:
        # Add cart after admin section
        old_text = '''{% if current_user.is_admin %}
            <a href="{{ url_for('admin_dashboard') }}">Admin</a>
            <a href="{{ url_for('admin_categories') }}">📁 Categories</a>
        {% endif %}'''
        
        new_text = '''{% if current_user.is_admin %}
            <a href="{{ url_for('admin_dashboard') }}">Admin</a>
            <a href="{{ url_for('admin_categories') }}">📁 Categories</a>
        {% endif %}
        <a href="{{ url_for('view_cart') }}">🛒 Cart</a>'''
        
        if old_text in content:
            content = content.replace(old_text, new_text)
            print("✅ Added cart link after admin section")
    
    # Write the updated template
    with open(template_path, 'w', encoding='utf-8') as file:
        file.write(content)
    
    print("🎉 CART NAVIGATION FIXED!")

if __name__ == '__main__':
    manual_fix()