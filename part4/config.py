import os
from datetime import timedelta


class DefaultAdmin:
    DEFAULT_HBNB_ADMIN_FIRST_NAME = 'Holberton'
    DEFAULT_HBNB_ADMIN_LAST_NAME = 'School'
    DEFAULT_HBNB_ADMIN_PASSWORD = 'Password123456789!'
    DEFAULT_HBNB_ADMIN_EMAIL = '{}.{}@localhost.local'.format(
            DEFAULT_HBNB_ADMIN_FIRST_NAME.lower(),
            DEFAULT_HBNB_ADMIN_LAST_NAME.lower()
            )


class Config:
    DEBUG = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', '_Dan_Florentin_872_')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_ALGORITHM = 'HS512'
    JWT_DECODE_ALGORITHMS = ['HS512']


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///development.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


config = {
        'development': DevelopmentConfig,
        'default': DevelopmentConfig,
        'admin': DefaultAdmin
        }

