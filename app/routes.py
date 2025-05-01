from flask import redirect, url_for, render_template, request, session
from app import db
from app.models import Details
from datetime import datetime

def setup_routes(app):
    @app.route('/')
    def home():
        return render_template('home.html')  # Add this file to templates

    # Additional routes can go here

    @app.route('/expense', methods=["POST", "GET"])
    def adding_data():
        if request.method == "POST":
            user_id = request.form["user_id"]
            amount = request.form["amount"]
            categorize = request.form["category"]
            description = request.form["description"]
            date_input = request.form["date"]
            valid_date = datetime.strptime(date_input, "%Y-%m-%d").date()

            new_input = Details(user_id=user_id, amount=amount, category=categorize, description=description, date=valid_date)
            db.session.add(new_input)
            db.session.commit()
            return render_template("forms.html")

        else:
            return render_template("forms.html")
            
