import os

def find_templates():
    print("🔍 FINDING TEMPLATE FILES...")
    
    # Check common template locations
    possible_paths = [
        'templates/base.html',
        'templates/base.html.txt',
        'base.html',
        '../templates/base.html',
        'app/templates/base.html'
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            print(f"✅ Found: {path}")
            return path
    
    # Search recursively
    print("🔍 Searching for template files...")
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file == 'base.html' or file == 'base.html.txt':
                full_path = os.path.join(root, file)
                print(f"✅ Found: {full_path}")
                return full_path
    
    print("❌ Could not find base.html template")
    return None

if __name__ == '__main__':
    template_path = find_templates()
    if template_path:
        print(f"\n🎯 Your template is at: {template_path}")
    else:
        print("\n❌ No template found. Let's check your project structure:")
        print("📁 Current directory contents:")
        for item in os.listdir('.'):
            print(f"   - {item}")