from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from myblog import db, login_manager
from flask_login import UserMixin # a class that cam be inherited from to add all 4 required user attribute

# user loader function for reloading user information by id
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    # function for getting reset token
    def get_reset_token(self, expires_sec=1800):
        # set unique serializer and expire parameter
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        # return serialized token
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod # tells python to not expect self argument
    def verify_reset_token(token):
        # set unique serializer
        s = Serializer(current_app.config['SECRET_KEY'])
        # try to load the token, return user_id if valid, else None
        try: 
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}, {self.email}, {self.image_file}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"User('{self.title}, {self.date_posted}')"