from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

db = SQLAlchemy()
login_manager = LoginManager()

def load_user(user_id):
    from .models import User  # Import here to avoid circular import
    return User.query.get(int(user_id))

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///D:\\Projects\\Max\\news_aggregator_web_app\\news-aggregator\\myflaskapp\\app.db'  # or your actual database URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # optional: reduces memory usage

    db.init_app(app)
    login_manager.init_app(app)
    Migrate(app, db)  # Initialize Flask-Migrate here without assigning it to a variable
    login_manager.user_loader(load_user)

    with app.app_context():
        db.create_all()  # create all database tables

    from .routes import routes as routes_blueprint
    app.register_blueprint(routes_blueprint)

    return app



