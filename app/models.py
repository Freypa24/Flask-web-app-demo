from functools import wraps
from flask import session, url_for, g, redirect
from app.database import db
from sqlalchemy import ForeignKey

"""
    Models are a term for postgres tables.
    Listed within this folder are the creation, dropping,
    or updating of tables.
"""


class User(db.Model):
    __tablename__ = "users"

    user_id = db.Column(db.INT, primary_key = True, nullable=False)
    full_name = db.Column(db.VARCHAR(255))
    email = db.Column(db.TEXT, unique=True, nullable=False)
    password = db.Column(db.TEXT, nullable=False)
    date_of_creation = db.Column(db.DATE, nullable=False)


def auth_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorator
