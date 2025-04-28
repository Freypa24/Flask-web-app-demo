import os
from os import environ

from dotenv import load_dotenv
from pathlib import Path

"""
    Settings.py is our configuration script that loads the .env variables
    and modifies the app's configuration.
"""


if not os.environ.get("SECRET_KEY"):
    env_path = Path(__file__).resolve().parent.parent / ".env"
    if env_path.exists():
        load_dotenv(dotenv_path=env_path)
        print("[INFO] Loaded local .env for development.")
    else:
        print("[INFO] No .env file found. Skipping local env load.")


class Config:
    SECRET_KEY = environ.get('SECRET_KEY')
    SESSION_COOKIE_NAME = environ.get('SESSION_COOKIE_NAME')

    # Database
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class DevConfig(Config):

    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = environ.get('CONTAINER_DATABASE_URL')


class TestConfig(Config):

    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = environ.get('CONTAINER_DATABASE_URL')


class ProdConfig(Config):

    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = environ.get('PROD_DATABASE_URL')
