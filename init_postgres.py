import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def init_postgres():
    # Get database URL from environment
    database_url = os.getenv('DATABASE_URL')
    
    if not database_url:
        print("❌ DATABASE_URL not found in environment variables")
        return
    
    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(database_url)
        conn.autocommit = True
        cursor = conn.cursor()
        
        print("✅ Connected to PostgreSQL successfully!")
        
        # Test connection
        cursor.execute("SELECT version();")
        db_version = cursor.fetchone()
        print(f"📊 PostgreSQL Version: {db_version[0]}")
        
        # Check if our database exists and is accessible
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        """)
        tables = cursor.fetchall()
        print(f"📋 Found {len(tables)} existing tables")
        
        print("✅ PostgreSQL initialization complete!")
        print("🚀 Start your application with: python app.py")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Error connecting to PostgreSQL: {e}")
        print("💡 Make sure PostgreSQL is running and DATABASE_URL is correct in .env file")

if __name__ == '__main__':
    init_postgres()