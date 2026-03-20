#!/bin/bash
set -e  # Stop on error
set -x  # Show every command

echo "=== STARTING CORNER DOOR ==="
pwd
ls -la

echo "=== INSTALLING DEPENDENCIES ==="
pip install --upgrade pip
pip install -r requirements.txt

echo "=== RUNNING APP ==="
python app.py
