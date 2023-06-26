from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import db
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True) 
    email = db.Column(db.String(120), nullable=False)
    password_hash = db.Column(db.String(128))
    bio = db.Column(db.Text, nullable=True)  # New field for biography
    profile_picture = db.Column(db.String(120), nullable=True)  # New field for profile picture
    role = db.Column(db.String(20), default='user')  # New field for user role with a default value
    __table_args__ = (db.UniqueConstraint('email', name='uix_1'), )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    role = SelectField('Role', choices=[('user', 'User'), ('admin', 'Admin')])  # Add the role field
    submit = SubmitField('Sign Up')


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200))
    link = db.Column(db.String(500))
    posted_timestamp = db.Column(db.DateTime)
    description = db.Column(db.String(2000))
    source_id = db.Column(db.Integer, db.ForeignKey('source.id'))
    category = db.Column(db.String(200))

    # Serialize method for Article
    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'link': self.link,
            'posted_timestamp': self.posted_timestamp,
            'description': self.description,
            'source_id': self.source_id,
            'category': self.category
        }

class Source(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    rss_feed_url = db.Column(db.String(500))
    articles = db.relationship('Article', backref='source', lazy=True)



