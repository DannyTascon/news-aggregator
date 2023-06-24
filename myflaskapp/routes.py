# routes.py
from flask import Blueprint, render_template, redirect, url_for, request, abort
from flask_login import login_user, logout_user, login_required
from .models import User, Article

routes = Blueprint('routes', __name__)

@routes.route('/')
def home():
    return render_template('home.html')

@routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember = request.form.get('remember')
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user, remember=remember)
            return redirect(url_for('routes.home'))  # modified here
    return render_template('login.html')

@routes.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('routes.home'))  # modified here

# New Route for retrieving a specific article
@routes.route('/articles/<int:article_id>', methods=['GET'])
def get_article(article_id):
    article = Article.query.get(article_id)
    if article is None:
        abort(404, description="Article not found")
    return render_template('article.html', article=article)

# ... existing code ...

@routes.route('/articles')
def articles():
    # Fetch all articles from the database
    articles = Article.query.all()

    # Render the articles template and pass the articles to it
    return render_template('articles.html', articles=articles)

# New routes

@routes.route('/register')
def register():
    return render_template('register.html')

@routes.route('/profile')
def profile():
    return render_template('profile.html')

@routes.route('/about')
def about():
    return render_template('about.html')

@routes.route('/contact')
def contact():
    return render_template('contact.html')

@routes.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404

@routes.errorhandler(500)
def internal_server_error(e):
    # note that we set the 500 status explicitly
    return render_template('500.html'), 500



