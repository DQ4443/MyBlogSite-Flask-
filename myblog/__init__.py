from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from myblog.config import Config


# the following processes initialize the imported extensions

# create db for User and Post data storage
db = SQLAlchemy()

# set up bcrypt to ensure user password security against data breaches
bcrypt = Bcrypt()

# set up login manager to help with user logins
login_manager = LoginManager()
# set login route
login_manager.login_view = 'users.login' # view is the function name of route
# set login message look
login_manager.login_message_category = 'info'


mail = Mail()



def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from myblog.users.routes import users
    from myblog.posts.routes import posts
    from myblog.main.routes import main
    from myblog.errors.handlers import errors
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app