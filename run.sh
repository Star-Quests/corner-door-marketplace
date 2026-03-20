#!/bin/bash
echo "=== Starting app ==="
cd /app
python -c "
import sys
import traceback
try:
    from app import app
    print('✅ App imported successfully')
except Exception as e:
    print('❌ App import failed:')
    traceback.print_exc()
    sys.exit(1)
"

# If import succeeded, start gunicorn
if [ $? -eq 0 ]; then
    echo "Starting gunicorn..."
    exec gunicorn app:app
else
    echo "Failed to import app, exiting"
    exit 1
fi
