from flask import render_template, request, Blueprint
from blog.models import Post

# exporting the MAIN package, imported by the flaskblog __init__ file, out main init file
main = Blueprint('main', __name__)


# using the BLUEPRINT name to replace "@app.route"
@main.route("/")
@main.route("/home")
def home():
    # default is 1 for page number
    page = request.args.get('page', 1, type=int) 
    # 5 post per page is preferred
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=2)
    return render_template('home.html', posts=posts)


@main.route('/about')
def about():
    return render_template('about.html', title='About')