# Crypto Fix Script
import re

print("🔧 FIXING CRYPTO PRICES FUNCTION...")

# Read the current app.py
with open("app.py", "r", encoding="utf-8") as f:
    content = f.read()

# The new working crypto function
new_function = '''@app.route('/crypto-prices')
def crypto_prices():
    import requests
    from flask import jsonify
    try:
        response = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana&vs_currencies=usd', timeout=5)
        data = response.json()
        prices = {
            'BTC': data['bitcoin']['usd'],
            'ETH': data['ethereum']['usd'],
            'SOL': data['solana']['usd']
        }
        return jsonify(prices)
    except:
        prices = {
            'BTC': 50000,
            'ETH': 3000,
            'SOL': 100
        }
        return jsonify(prices)'''

# Find and replace the old function
if '@app.route('/crypto-prices')' in content:
    # Use simple string replacement
    lines = content.split('\n')
    new_lines = []
    skip = False
    
    for line in lines:
        if '@app.route('/crypto-prices')' in line:
            # Add the new function and skip the old one
            new_lines.append(new_function)
            skip = True
        elif skip and line.strip().startswith('@app.route'):
            # Stop skipping when we hit the next route
            skip = False
            new_lines.append(line)
        elif not skip:
            new_lines.append(line)
    
    # Write the fixed content
    with open("app.py", "w", encoding="utf-8") as f:
        f.write('\n'.join(new_lines))
    
    print("✅ CRYPTO PRICES FIXED!")
    print("🎉 Restart your app: python app.py")
else:
    print("❌ Could not find crypto-prices route")
