import os

def fix_cart_exact():
    print("🔧 FIXING CART NAVIGATION WITH EXACT PATH...")
    
    # Use the exact path we found earlier
    template_path = r'.\Desktop\Apps i have developed\corner_door\templates\base.html'
    
    if not os.path.exists(template_path):
        print("❌ Template not found at exact path. Let me search...")
        # Search for it
        for root, dirs, files in os.walk('.'):
            for file in files:
                if file == 'base.html':
                    full_path = os.path.join(root, file)
                    print(f"✅ Found template at: {full_path}")
                    template_path = full_path
                    break
    
    if not os.path.exists(template_path):
        print("❌ Still cannot find template. Let's check current directory:")
        print("📁 Current directory:", os.getcwd())
        print("📁 Contents:")
        for item in os.listdir('.'):
            print(f"   - {item}")
        return
    
    print(f"✅ Working with template: {template_path}")
    
    # Read the template
    with open(template_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Check if cart link already exists
    if '🛒 Cart' in content:
        print("✅ Cart link already exists in navigation!")
        return
    
    # Add cart link to navigation
    print("🔧 Adding cart link to navigation...")
    
    # Method 1: Add after admin section
    if '{% if current_user.is_admin %}' in content:
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
    
    # Method 2: Add after search link (if method 1 didn't work)
    elif '🔍 Search' in content and '🛒 Cart' not in content:
        old_text = '''<a href="{{ url_for('search') }}">🔍 Search</a>
        {% if current_user.is_authenticated %}'''
        
        new_text = '''<a href="{{ url_for('search') }}">🔍 Search</a>
        {% if current_user.is_authenticated %}
            <a href="{{ url_for('view_cart') }}">🛒 Cart</a>'''
        
        if old_text in content:
            content = content.replace(old_text, new_text)
            print("✅ Added cart link after search")
    
    # Write the updated template
    with open(template_path, 'w', encoding='utf-8') as file:
        file.write(content)
    
    print("🎉 CART NAVIGATION FIXED!")
    print("Please restart your app: python app.py")

if __name__ == '__main__':
    fix_cart_exact()