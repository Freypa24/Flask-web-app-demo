from app import create_app
from app.database import db
from app.models import User, Workforce
from werkzeug.security import generate_password_hash
import datetime


def create_admin():
    existing_admin = User.query.filter_by(email="admin@example.com").first()
    if not existing_admin:
        hashed_password = generate_password_hash("admin123")  # Change to secure password
        existing_admin = User(
            full_name="Admin User",
            email="admin@example.com",
            password=hashed_password,
            role="admin",
            date_of_creation=datetime.date.today()
        )
        db.session.add(existing_admin)
        db.session.commit()
        print("✅ Admin user created")
    else:
        print("⚠️ Admin already exists.")

    existing_workforce = Workforce.query.filter_by(name="IT Department").first()
    if not existing_workforce:
        workforce = Workforce(
            name="IT Department"
        )
        workforce.admins.append(existing_admin)
        db.session.add(workforce)
        db.session.commit()
        print("✅ Workforce created and assigned to admin")
    else:
        print("⚠️ Workforce already exists.")


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        create_admin()