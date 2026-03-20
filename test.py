#!/usr/bin/env python
"""Minimal test app - just to check if Flask works"""

import os
import sys

print("=" * 60)
print("TEST APP STARTING")
print(f"Python: {sys.version}")
print(f"Working dir: {os.getcwd()}")
print(f"Files: {os.listdir('.')}")
print("=" * 60)

from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return """
    <h1>✅ CORNER DOOR MARKETPLACE - TEST MODE</h1>
    <p>If you see this, Flask is working!</p>
    <p>Now check your main app for errors.</p>
    """

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
