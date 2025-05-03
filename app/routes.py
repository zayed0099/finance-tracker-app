from flask import redirect, url_for, render_template, request, session
from app import db
from app.models import Details
from datetime import datetime

def setup_routes(app):
    @app.route('/')
    def home():
        return render_template('home.html')  # Add this file to templates

    # Additional routes can go here

    # @app.route('/add_expense', methods=["POST", "GET"])
    # def adding_data():
    #     if request.method == "POST":
    #         user_id = request.form["user_id"]
    #         amount = request.form["amount"]
    #         categorize = request.form["category"]
    #         description = request.form["description"]
    #         date_input = request.form["date"]
    #         valid_date = datetime.strptime(date_input, "%Y-%m-%d").date()

    #         new_input = Details(user_id=user_id, amount=amount, category=categorize, description=description, date=valid_date)
    #         db.session.add(new_input)
    #         db.session.commit()
    #         return render_template("forms.html")

    #     else:
    #         return render_template("forms.html")

    @app.route('/view', methods=["POST", "GET"])
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
            return redirect(url_for('adding_data'))  # Redirect to the same page
        
        all_details = Details.query.all()
        return render_template("view.html", details=all_details)
        
    @app.route('/debug')
    def debug_db():
        details = Details.query.all()
        return "<br>".join([f"{d.user_id} - {d.amount} - {d.category}" for d in details])
      





















    #     filter_option = request.args.get('filter')
    #     results = []

    #     if filter_option == 'amount':
    #         db.query_amount()
    #     elif filter_option == 'category':
    #         db.query_category()
    #     elif filter_option == 'date':
    #         db.quer_date()
    #     else:
    #         results = ['No matching filter.']

    #     return render_template('filter_page.html', results=results)









    