from flask import redirect, url_for, render_template, request, session
from app.models import Details

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
            date = request.form["date"]
            
            new_input = Details(amount=amount, categorize=category, description=description, date=date)
            db.session.add(new_input)
            db.session.commit()

        else:
            return render_template("forms.html")
            
