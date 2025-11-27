from app import app, db, User
from werkzeug.security import generate_password_hash

def create_new_admin():
    with app.app_context():
        # Check if admin already exists
        existing_admin = User.query.filter_by(username='newadmin').first()
        if not existing_admin:
            # Create new admin
            admin = User(
                username='newadmin',
                password_hash=generate_password_hash('newadmin123'),
                is_admin=True,
                is_active=True,
                recovery_phrase='new admin account'
            )
            db.session.add(admin)
            db.session.commit()
            print("New admin created: username='newadmin', password='newadmin123'")
        else:
            print("Admin already exists")

if __name__ == '__main__':
    create_new_admin()