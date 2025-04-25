from os import environ, path

from dotenv import load_dotenv

"""
    Settings.py is our configuration script that loads the .env variables
    and modifies the app's configuration.
"""


def load_env():
    try:
        basedir = path.normpath(path.dirname(__file__))
        dotenv_path = load_dotenv(path.join(basedir, "..", '.env'))
    except Exception as e:
        print(f"[WARNING] - .env file could not be loaded at {dotenv_path}")


load_env()


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
