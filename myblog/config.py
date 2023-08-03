import os

class Config:
    # secret key for security
    SECRET_KEY = 'aecf24c4b1c207b387da5653dd54c59b'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'

    # config for sending emails
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')