import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

# default app to name of Flask process
app = Flask(__name__)

# secret key for security
app.config['SECRET_KEY'] = 'aecf24c4b1c207b387da5653dd54c59b'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

# the following processes initialize the imported extensions

# create db for User and Post data storage
db = SQLAlchemy(app)

# set up bcrypt to ensure user password security against data breaches
bcrypt = Bcrypt(app)

# set up login manager to help with user logins
login_manager = LoginManager(app)
# set login route
login_manager.login_view = 'login' # view is the function name of route
# set login message look
login_manager.login_message_category = 'info'

# config for sending emails
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')
mail = Mail(app)

from myblog import routes