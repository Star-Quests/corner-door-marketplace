#!/usr/bin/env python
"""Wrapper to catch errors and keep app running"""

import sys
import os
import traceback

# Force all output to be visible
sys.stdout = sys.stderr

print("=" * 60)
print("RUN.PY - Starting with error handling")
print("=" * 60)

try:
    # Try to import your main app
    print("Attempting to import app...")
    from app import app
    
    print("✅ App imported successfully!")
    print("Starting Flask server...")
    
    # Run the app
    app.run(host='0.0.0.0', port=5000, debug=False)
    
except Exception as e:
    print("=" * 60)
    print("❌ ERROR DETECTED - App failed to start")
    print("=" * 60)
    print(f"Error: {e}")
    print("\nFull traceback:")
    traceback.print_exc()
    print("=" * 60)
    
    # Don't crash - start a fallback app
    print("\nStarting fallback server to show error...")
    from flask import Flask
    fallback = Flask(__name__)
    
    @fallback.route('/')
    def error_page():
        return f"""
        <!DOCTYPE html>
        <html>
        <head><title>CORNER DOOR - Error</title></head>
        <body style="background:#0a0a0a; color:#e0e0e0; font-family:monospace; padding:20px;">
            <h1 style="color:#ff4444;">⚠️ Application Error</h1>
            <p>Your app failed to start. Here's the error:</p>
            <pre style="background:#1a1a1a; padding:15px; border-radius:5px; overflow:auto;">
{str(e)}

{traceback.format_exc()}
            </pre>
            <p>Fix the error above and redeploy.</p>
            <hr>
            <p><small>CORNER DOOR Marketplace - Debug Mode</small></p>
        </body>
        </html>
        """
    
    fallback.run(host='0.0.0.0', port=5000)
