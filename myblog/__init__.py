from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

# default app to name of Flask process
app = Flask(__name__)

# secret key for security
app.config['SECRET_KEY'] = 'aecf24c4b1c207b387da5653dd54c59b'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

# create db for User and Post data storage
db = SQLAlchemy(app)

# set up bcrypt to ensure user password security against data breaches
bcrypt = Bcrypt(app)

from myblog import routes