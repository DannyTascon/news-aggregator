from flask import Blueprint, render_template, redirect, url_for, request, abort, flash, current_app
from flask_login import login_user, logout_user, login_required, current_user
from .models import User, Article
from .forms import SubmitArticleForm, RegistrationForm, UpdateProfileForm, SearchForm
from . import db
from werkzeug.utils import secure_filename
import os
from .forms import SettingsForm
from flask import jsonify


routes = Blueprint('routes', __name__)

@routes.route('/')
def home():
    return render_template('home.html')

@routes.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('routes.home'))
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember = request.form.get('remember')
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user, remember=remember)
            return redirect(url_for('routes.home'))
    return render_template('login.html')

@routes.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('routes.home'))

@routes.route('/articles/<int:article_id>', methods=['GET'])
def get_article(article_id):
    article = Article.query.get(article_id)
    if article is None:
        abort(404, description="Article not found")
    return render_template('article.html', article=article)

@routes.route('/articles')
def articles():
    articles = Article.query.all()
    return render_template('articles.html', articles=articles)

@routes.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('routes.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('routes.login'))
    return render_template('register.html', title='Register', form=form)

@routes.route('/profile/update', methods=['GET', 'POST'])
@login_required
def update_profile():
    form = UpdateProfileForm()

    if form.validate_on_submit():
        current_user.bio = form.bio.data

        if form.profile_picture.data:
            filename = secure_filename(form.profile_picture.data.filename)
            form.profile_picture.data.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            current_user.profile_picture = filename

        db.session.commit()
        flash('Your profile has been updated!', 'success')
        return redirect(url_for('routes.profile'))

    form.bio.data = current_user.bio

    return render_template('update_profile.html', title='Update Profile', form=form)

@routes.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)

@routes.route('/about')
def about():
    return render_template('about.html')

@routes.route('/contact')
def contact():
    return render_template('contact.html')

@routes.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@routes.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@routes.route('/submit_article', methods=['GET', 'POST'])
@login_required
def submit_article():
    form = SubmitArticleForm()
    if form.validate_on_submit():
        new_article = Article(
            title=form.title.data,
            link=form.link.data,
            description=form.description.data,
            category=form.category.data
        )

        db.session.add(new_article)
        db.session.commit()
        return redirect(url_for('routes.home'))
    return render_template('submit_article.html', form=form)

@routes.route('/edit_article/<int:article_id>', methods=['GET', 'POST'])
@login_required
def edit_article(article_id):
    article = Article.query.get_or_404(article_id)

    if article.author != current_user:
        abort(403)  # Forbidden access

    form = SubmitArticleForm()

    if form.validate_on_submit():
        article.title = form.title.data
        article.link = form.link.data
        article.description = form.description.data
        article.category = form.category.data

        db.session.commit()
        flash('Article has been updated!', 'success')
        return redirect(url_for('routes.articles'))

    # Pre-fill the form fields with the existing article data
    form.title.data = article.title
    form.link.data = article.link
    form.description.data = article.description
    form.category.data = article.category

    return render_template('edit_article.html', title='Edit Article', form=form)


@routes.route('/delete_article/<int:article_id>', methods=['POST'])
@login_required
def delete_article(article_id):
    article = Article.query.get_or_404(article_id)

    if article.author != current_user:
        abort(403)  # Forbidden access

    db.session.delete(article)
    db.session.commit()
    flash('Article has been deleted!', 'success')
    return redirect(url_for('routes.articles'))


@routes.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchForm()

    if form.validate_on_submit():
        search_query = form.search_query.data

        # Perform the search query on your database
        search_results = perform_search(search_query)

        return render_template('search.html', form=form, search_results=search_results, user=current_user)

    return render_template('search.html', form=form, user=current_user)

def perform_search(search_query):
    # Perform the necessary database query to retrieve search results
    # based on the search query
    search_results = Article.query.filter(Article.title.ilike(f"%{search_query}%")).all()
    return search_results


@routes.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    form = SettingsForm()

    if form.validate_on_submit():
        # Update the user's settings in the database
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.set_password(form.new_password.data)
        current_user.bio = form.bio.data

        if form.profile_picture.data:
            # Save the uploaded profile picture
            filename = secure_filename(form.profile_picture.data.filename)
            form.profile_picture.data.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            current_user.profile_picture = filename

        db.session.commit()
        flash('Your settings have been updated!', 'success')
        return redirect(url_for('routes.settings'))

    # Pre-fill the form fields with the current user's data
    form.username.data = current_user.username
    form.email.data = current_user.email
    form.bio.data = current_user.bio

    return render_template('settings.html', title='Account Settings', form=form)

@routes.route('/test_db')
def test_db():
    try:
        users = User.query.all()
        return jsonify({'users': [str(user) for user in users]}), 200  # A list of string representations of User objects
    except Exception as e:
        return str(e), 500



