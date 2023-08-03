import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

# default app to name of Flask process
app = Flask(__name__)


# the following processes initialize the imported extensions

# create db for User and Post data storage
db = SQLAlchemy(app)

# set up bcrypt to ensure user password security against data breaches
bcrypt = Bcrypt(app)

# set up login manager to help with user logins
login_manager = LoginManager(app)
# set login route
login_manager.login_view = 'users.login' # view is the function name of route
# set login message look
login_manager.login_message_category = 'info'


mail = Mail(app)

from myblog.users.routes import users
from myblog.posts.routes import posts
from myblog.main.routes import main

app.register_blueprint(users)
app.register_blueprint(posts)
app.register_blueprint(main)