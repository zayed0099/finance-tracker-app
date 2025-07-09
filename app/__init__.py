from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)

    # secret key set-up
    app.secret_key = 'we_steal_mangoes'
   
    # This line gets the full path to the app folder
    basedir = os.path.abspath(os.path.dirname(__file__))

    # Tell Flask-SQLAlchemy to place app.db inside the app folder
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)

    from . import models  # Import models so Flask knows about the tables. importing tables from models.py and creating them here

    with app.app_context():
        # Print the actual DB path
        db_path = app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', '')
        print("🔍 Using database file at:", os.path.abspath(db_path))

        db.create_all()
    
    from app.models import User

    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))


    login_manager.login_view = 'login'
       
    # Register routes here
    from app.routes import setup_routes
    setup_routes(app)

    return app
