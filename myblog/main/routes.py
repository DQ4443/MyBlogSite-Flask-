from flask import Blueprint
from flask import render_template, request
from myblog.models import Post

main = Blueprint('main', __name__)

# home by default
@main.route("/")
@main.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    # order_by changes post order function; paginate 
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=3)
    return render_template('home.html', posts=posts)

@main.route("/about")
def about():
    return render_template('about.html', title="About")