from flask import Blueprint
from flask import render_template, url_for, flash, redirect, request, abort
from myblog import db# importing from package imports from init file
from myblog.posts.forms import PostForm
from myblog.models import Post
from flask_login import current_user, login_required

posts = Blueprint('posts', __name__)

# route for making new posts
@posts.route("/post/new", methods=['GET', 'POST'])
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
@posts.route("/post/<int:post_id>")
def post(post_id):
    # return 404 if post doesn't exist
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title='post.title', post=post)


# route for updating a post
@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
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

@posts.route("/post/<int:post_id>/delete", methods=['POST'])
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