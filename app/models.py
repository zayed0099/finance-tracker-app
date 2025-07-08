from . import db
from datetime import date

# we will only create the tables here. all the other works will be done in init.py
class User(db.Model):
    __tablename__ = 'user_db'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), default="user", nullable=False)
 
    details = db.relationship('Details', backref='user', lazy=True)


class Details(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(200))
    date = db.Column(db.Date, default=date.today)

    user_id = db.Column(db.Integer, db.ForeignKey('user_db.id'), index=True, nullable=False)
