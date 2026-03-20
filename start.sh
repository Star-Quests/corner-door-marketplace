#!/bin/bash
echo "Starting CORNER DOOR Marketplace..."
echo "PORT: $PORT"
echo "Python version: $(python --version)"
echo "Installed packages:"
pip list | grep -E "Flask|gunicorn|psycopg2"

# Run database setup
python -c "from app import app, db; app.app_context().push(); db.create_all(); print('Database ready')"

# Start the app
exec gunicorn --bind 0.0.0.0:$PORT app:app
