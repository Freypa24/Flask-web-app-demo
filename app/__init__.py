from os import environ

from flask import Flask
from sqlalchemy import text

from app.database import db, migrate
from app.routes import user_bp, template_bp, auth_bp
from app.settings import DevConfig, TestConfig, ProdConfig


def create_app(config_class=None):
    app = Flask(__name__)

    if config_class is None:
        config_class = environ.get('CONFIG_ENV', 'development').lower()

    match config_class:
        case "development":
            app.config.from_object(DevConfig)
            db.init_app(app)
        case "testing":
            app.config.from_object(TestConfig)
            db.init_app(app)
        case "production":
            app.config.from_object(ProdConfig)
            db.init_app(app)
        case _:
            raise ValueError(f"Invalid configuration class specified. value of config_class is - {config_class}")

    migrate.init_app(app, db)

    _register_blueprints(app)

    with app.app_context():
        try:
            # 👇 This is a real query to test connection
            db.session.execute(text('SELECT 1'))
            print("✅ Connected to Postgres!", db)
        except Exception as e:
            print("❌ Failed to connect to Postgres:", e)

    return app


def _register_blueprints(app):
    app.register_blueprint(user_bp)
    app.register_blueprint(template_bp)
    app.register_blueprint(auth_bp)
