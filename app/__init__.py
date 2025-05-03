from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
   
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
        
    # Register routes here
    from app.routes import setup_routes
    setup_routes(app)

    return app
