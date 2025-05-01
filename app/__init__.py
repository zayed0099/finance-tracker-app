from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from app.routes import setup_routes

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    from . import models  # Import models so Flask knows about the tables

    with app.app_context():
        db.create_all()

    return app
