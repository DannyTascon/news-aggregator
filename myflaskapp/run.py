from myflaskapp import create_app, db
from myflaskapp.models import User
from flask_migrate import Migrate
from flask import Flask

app = create_app()
app.debug = True

migrate = Migrate(app, db)

from myflaskapp import login_manager
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    return "Hello, world!"




