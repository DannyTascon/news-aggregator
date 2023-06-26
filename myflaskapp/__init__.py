from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'SoccerBall2023!!'  # Add this line with your own secret key
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///D:\\Projects\\Max\\news_aggregator_web_app\\news-aggregator\\myflaskapp\\app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


    db.init_app(app)
    login_manager.init_app(app)
    Migrate(app, db)  # Initialize Flask-Migrate here without assigning it to a variable

    with app.app_context():
        db.create_all()  # create all database tables

    print(app.url_map)  # print all registered routes

    from .api import api_bp  # import the Blueprint instance
    app.register_blueprint(api_bp, url_prefix='/api')  # register the Blueprint instance with url prefix /api
    print(app.url_map)  # print all registered routes

    from .routes import routes as routes_blueprint
    app.register_blueprint(routes_blueprint)
    print(app.url_map)  # print all registered routes again

    return app

@login_manager.user_loader
def load_user(user_id):
    from .models import User  # Import here to avoid circular import
    return User.query.get(int(user_id))









