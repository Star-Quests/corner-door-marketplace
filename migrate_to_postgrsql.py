import os
import sqlite3
import psycopg2
from urllib.parse import urlparse

def migrate_to_postgresql():
    print("🚀 MIGRATING FROM SQLITE TO POSTGRESQL...")
    
    # Get PostgreSQL connection from environment
    database_url = os.environ.get('DATABASE_URL')
    if not database_url:
        print("❌ DATABASE_URL environment variable not set")
        return
    
    # Parse the database URL
    result = urlparse(database_url)
    username = result.username
    password = result.password
    database = result.path[1:]
    hostname = result.hostname
    port = result.port
    
    try:
        # Connect to SQLite
        sqlite_conn = sqlite3.connect('corner_door.db')
        sqlite_cursor = sqlite_conn.cursor()
        
        # Connect to PostgreSQL
        pg_conn = psycopg2.connect(
            database=database,
            user=username,
            password=password,
            host=hostname,
            port=port
        )
        pg_cursor = pg_conn.cursor()
        
        # Get all tables from SQLite
        sqlite_cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [table[0] for table in sqlite_cursor.fetchall()]
        
        print(f"📊 Found tables: {tables}")
        
        for table in tables:
            if table == 'sqlite_sequence':
                continue
                
            print(f"🔄 Migrating table: {table}")
            
            # Get data from SQLite
            sqlite_cursor.execute(f"SELECT * FROM {table}")
            rows = sqlite_cursor.fetchall()
            
            # Get column names
            sqlite_cursor.execute(f"PRAGMA table_info({table})")
            columns = [col[1] for col in sqlite_cursor.fetchall()]
            
            if rows:
                # Create placeholders for INSERT
                placeholders = ', '.join(['%s'] * len(columns))
                columns_str = ', '.join(columns)
                
                # Insert data into PostgreSQL
                for row in rows:
                    try:
                        pg_cursor.execute(
                            f"INSERT INTO {table} ({columns_str}) VALUES ({placeholders})",
                            row
                        )
                    except Exception as e:
                        print(f"⚠️  Could not insert row into {table}: {e}")
                        continue
            
            print(f"✅ Migrated {len(rows)} rows from {table}")
        
        # Commit changes
        pg_conn.commit()
        
        print("🎉 MIGRATION COMPLETED SUCCESSFULLY!")
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Close connections
        if 'sqlite_conn' in locals():
            sqlite_conn.close()
        if 'pg_conn' in locals():
            pg_conn.close()

if __name__ == '__main__':
    migrate_to_postgresql()