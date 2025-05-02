from functools import wraps
from flask import session, url_for, redirect
from app.database import db
from sqlalchemy import ForeignKey

"""
    Models are a term for postgres tables.
    Listed within this folder are the creation, dropping,
    or updating of tables.
"""

# join table
workforce_admins = db.Table(
    'workforce_admins',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('workforce_id', db.Integer, db.ForeignKey('workforces.id'), primary_key=True)
)


class Workforce(db.Model):
    __tablename__ = "workforces"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(150), nullable=False, unique=True)

    employees = db.relationship("User", back_populates="workforce")

    # admins relationship via join table
    admins = db.relationship(
        'User',
        secondary=workforce_admins,
        backref='administered_workforces'
    )


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.INT, primary_key = True, nullable=False)
    full_name = db.Column(db.VARCHAR(255))
    email = db.Column(db.TEXT, unique=True, nullable=False)
    password = db.Column(db.TEXT, nullable=False)
    role = db.Column(db.VARCHAR(50), nullable=False, default='employee')

    workforce_id = db.Column(db.INT, db.ForeignKey('workforces.id'), nullable=True)
    workforce = db.relationship('Workforce', back_populates='employees')

    date_of_creation = db.Column(db.DATE, nullable=False)

    @property
    def is_admin(self):
        return self.role == "admin"

    __table_args__ = (
        db.CheckConstraint(
            role.in_(['admin', 'employee']),
            name='check_user_role_valid'
        ),
    )


def auth_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorator


def admin_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        if 'user_id' not in session or session.get('role') != 'admin':
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorator

def employee_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        if "user_id" not in session or session.get('role') != "employee":
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return decorator
