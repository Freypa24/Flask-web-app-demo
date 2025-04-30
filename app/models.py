from functools import wraps
from flask import session, url_for, g, redirect
from app.database import db
from sqlalchemy import ForeignKey

"""
    Models are a term for postgres tables.
    Listed within this folder are the creation, dropping,
    or updating of tables.
"""

"""
class Workforce(db.Model):
    __tablename__ = "workforces"

    id = db.Column(db.INT, primary_key=True, nullable=False)
    name = db.Column(db.VARCHAR(150), nullable=False, unique=True)
    admin_id = db.Column(db.INT, db.ForeignKey['users.id'], nullable=True)
    admin = db.relationship('User', backref="manages_workforce", foreign_keys=[admin_id])
    employees = db.relationship("User", back_populates="workforce", foreign_keys[User.wo])
"""

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.INT, primary_key = True, nullable=False)
    full_name = db.Column(db.VARCHAR(255))
    email = db.Column(db.TEXT, unique=True, nullable=False)
    password = db.Column(db.TEXT, nullable=False)
    role = db.Column(db.VARCHAR(50), nullable=False, default='employee')
    """
    workforce_id = db.Column(db.INT, db.ForeignKey('workforces.id'), nullable=True)
    workforce = db.relationship('Workforce', back_populates='employees')
    """
    date_of_creation = db.Column(db.DATE, nullable=False)

    """
    __table_args__ = (
        db.CheckConstraint(
            role.in_(['admin', 'employee']),
            name='check_user_role_valid'
        ),
    )
    """


def auth_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.signin_page'))
        return f(*args, **kwargs)
    return decorator

"""
def admin_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        if 'user_id' not in session:
            return 
"""