from flask import Blueprint
from flask import render_template, url_for, flash, redirect, request
from myblog import db, bcrypt # importing from package imports from init file
from myblog.users.forms import RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm
from myblog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
from myblog.users.utils import save_picture, send_reset_email

users = Blueprint('users', __name__)

@users.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
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
        return redirect(url_for('main.login'))
    return render_template('register.html', title='Register', form=form)

@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            # get next parameter, which is what the next page should be. default to None
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Invalid login credentials, please try again.', 'danger')
    return render_template('login.html', title='Login', form=form)

# log user out
@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))

# account section route
@users.route("/account", methods=['GET', 'POST'])
# need to login to access that route
@login_required
def account():
    form = UpdateAccountForm()
    # if form submit was valid, update corresponding info in db
    if form.validate_on_submit():
        # picture field is not required
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account information has been updated', 'success')
        return redirect(url_for('users.account'))
    # if GET request (when user views without updating), auto fill in current information
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    # image_file variable from static folder
    image_file = url_for('static', filename='flask profile pictures/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)

# route for user page when user clicks on post author link
@users.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    # order_by changes post order function; paginate 
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(page=page, per_page=3)
    return render_template('user_posts.html', posts=posts, user=user)

@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('main.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)

@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if not user:
        flash('That is not a valid token. Please click on the link sent to you via email for your provided email address.', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        # flash a message to tell user it was successful
        flash(f'Your password has been updated! You are now able to log in :D', 'success')
        #redirect to log in page
        return redirect(url_for('main.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)