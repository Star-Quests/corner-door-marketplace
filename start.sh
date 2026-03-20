#!/bin/bash
echo "=== Starting Corner Door ==="
echo "Current directory: $(pwd)"
echo "Python version: $(python --version)"
echo "Files in directory:"
ls -la
echo "Testing import of app..."
python -c "import app; print('Import successful')"
echo "Starting Flask app..."
exec python app.py
