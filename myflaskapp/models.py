from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200))
    link = db.Column(db.String(500))
    posted_timestamp = db.Column(db.DateTime)
    description = db.Column(db.String(2000))
    source_id = db.Column(db.Integer, db.ForeignKey('source.id'))
    category = db.Column(db.String(200))

class Source(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    rss_feed_url = db.Column(db.String(500))
    articles = db.relationship('Article', backref='source', lazy=True)


