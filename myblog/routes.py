import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from myblog import app, db, bcrypt # importing from package imports from init file
from myblog.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm, RequestResetForm, ResetPasswordForm
from myblog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required

# home by default
@app.route("/")
@app.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    # order_by changes post order function; paginate 
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=3)
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
            # get next parameter, which is what the next page should be. default to None
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Invalid login credentials, please try again.', 'danger')
    return render_template('login.html', title='Login', form=form)

# log user out
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

#   function for saving pictures
def save_picture(form_picture):
    # generates 8 byte hex
    random_hex = secrets.token_hex(8)
    # get name and ext of file
    _, f_ext = os.path.splitext(form_picture.filename)
    # concatenate
    picture_fn = random_hex + f_ext
    # get full path of picture location 
    picture_path = os.path.join(app.root_path, 'static/flask profile pictures', picture_fn)

    # resize image with Pillow before saving
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)

    i.save(picture_path)
    # returns file name
    return picture_fn


# account section route
@app.route("/account", methods=['GET', 'POST'])
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
        return redirect(url_for('account'))
    # if GET request (when user views without updating), auto fill in current information
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    # image_file variable from static folder
    image_file = url_for('static', filename='flask profile pictures/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)

# route for making new posts
@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        # add post to db and attach to db
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post', form=form, legend='New Post')


# route for each specific post
@app.route("/post/<int:post_id>")
def post(post_id):
    # return 404 if post doesn't exist
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title='post.title', post=post)


# route for updating a post
@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    # return 403 if user is not author of post
    if current_user != post.author:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        # don't need db.session.ad because the data is already in the database
        db.session.commit()
        flash('Your post has been updated.', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        # fill in form with post data
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post', form=form, legend='Update Post')

@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    # return 403 if user is not author of post
    if current_user != post.author:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted.', 'success')
    return redirect(url_for('home'))

# route for user page when user clicks on post author link
@app.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    # order_by changes post order function; paginate 
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(page=page, per_page=3)
    return render_template('user_posts.html', posts=posts, user=user)

# method for sending a reset password email to the given user
def send_reset_email(user):
    pass

@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset Password', form=form)

@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if not user:
        flash('That is not a valid token. Please click on the link sent to you via email for your provided email address.', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    return render_template('reset_token.html', title='Reset Password', form=form)


    