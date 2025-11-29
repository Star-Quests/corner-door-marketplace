import os

def verify_cart():
    print("🔍 VERIFYING CART LINK...")
    
    # Try multiple possible paths
    paths_to_check = [
        r'.\templates\base.html',
        r'..\templates\base.html', 
        r'C:\Users\EMIOLA\Desktop\Apps i have developed\corner_door\templates\base.html'
    ]
    
    for path in paths_to_check:
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
                if '🛒 Cart' in content:
                    print(f"✅ SUCCESS! Cart link found in: {path}")
                    return True
                else:
                    print(f"❌ Cart link NOT found in: {path}")
    
    print("❌ Could not verify cart link. Please check manually.")
    return False

if __name__ == '__main__':
    verify_cart()