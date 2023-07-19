from flask import render_template, url_for, flash, redirect
from myblog import app, db, bcrypt # importing from package imports from init file
from myblog.forms import RegistrationForm, LoginForm
from myblog.models import User, Post
from flask_login import login_user, current_user


posts = [
    {
        'author': 'Jake Sully',
        'title': 'First Post',
        'content': 'I am blue...',
        'date_posted': 'April 20, 2022'
    },
    {
        'author': 'Neteyam Sully',
        'title': 'Second Post',
        'content': 'I am also blue... and have five fingers',
        'date_posted': 'April 22, 2022'
    }
]

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)

@app.route("/about")
def about():
    return render_template('about.html', title="About")

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    # if registration fields were correctly completed
    if form.validate_on_submit():
        # hash user password
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        # add a new user to db with username email and password
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        # flash a message to tell user it was successful
        flash(f'Account created for {form.username.data}! You are now able to log in :D', 'success')
        #redirect to log in page
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('home'))
        else:
            flash('Invalid login credentials, please try again.', 'danger')
    return render_template('login.html', title='Login', form=form)