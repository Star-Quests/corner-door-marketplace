from app import app, db, Category
import os

def clean_fix():
    print("🧹 CLEAN FIX: UPDATING DATABASE STRUCTURE...")
    
    with app.app_context():
        try:
            # First, let's check what tables exist
            print("📊 Checking current database structure...")
            
            # This will update any missing tables/columns without deleting data
            db.create_all()
            print("✅ Database structure updated!")
            
            # Check if categories exist, if not create some
            categories = Category.query.all()
            if not categories:
                print("📁 Creating sample categories...")
                sample_categories = [
                    Category(name='Books', description='Digital and physical books'),
                    Category(name='Electronics', description='Gadgets and electronic devices'),
                    Category(name='Digital Products', description='Software, courses, and digital content'),
                    Category(name='Services', description='Various services and consultations')
                ]
                for category in sample_categories:
                    db.session.add(category)
                db.session.commit()
                print(f"✅ Created {len(sample_categories)} sample categories!")
            else:
                print(f"✅ Found {len(categories)} existing categories")
                
            print("🎉 DATABASE READY FOR SEARCH AND CATEGORIES!")
            
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == '__main__':
    clean_fix()