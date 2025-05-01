from . import db
from datetime import date

# we will only create the tables here. all the other works will be done in init.py

class Details(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.String(10), unique=False, nullable=False)
    category = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(200))
    date = db.Column(db.Date, default=date.today)
