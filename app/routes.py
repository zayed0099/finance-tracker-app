from flask import redirect, url_for, render_template, request, session
from app import db
from app.models import Details
from datetime import datetime
from sqlalchemy import or_, cast, String

def setup_routes(app):
    @app.route('/')
    def home():
        return render_template('home.html')  # Add this file to templates

    # Additional routes can go here

    @app.route('/manage-expense', methods=["POST", "GET"])
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

    @app.route('/dashboard', methods=["POST", "GET"])
    def filter_data():
        if request.method == "POST":
            user_input = request.form["fil_data"]
            search_term = f"%{user_input}%"
            user_input = request.form.get("fil_data", "").strip()
            
            if user_input:
                # ... apply search filter
                filtered_users = Details.query.filter(
                    or_(
                        Details.user_id.ilike(search_term),
                        cast(Details.amount, String).ilike(search_term), #cant use them directly because amount and date are not string so need to make them string using cast
                        Details.category.ilike(search_term),
                        Details.description.ilike(search_term),
                        cast(Details.date, String).ilike(search_term)
                    )
                ).all()
                return render_template("filter.html", details=filtered_users, id=id)
            else:
                # return all records or a message
                all_details = Details.query.all()
                return render_template("filter.html", details=all_details)

        return render_template("filter.html")

    @app.route("/manage-expense/update/<int:id>", methods=["POST", "GET"])
    def update_data(id):
        user_to_update = Details.query.get_or_404(id)
        if request.method == "POST":
            user_to_update.amount = request.form['amount']
            db.session.commit()
            user_to_update.description == request.form['description']
            db.session.commit()
            user_to_update.category == request.form['category']
            db.session.commit()
            return render_template("filter.html")
        else:
            return render_template("update.html", id=id)



# Testing
    # @app.route("/test")
    # def test():
    #     return render_template('update.html')

    # @app.route('/debug-2955')
    # def debug_db():
    #     details = Details.query.all()
    #     return "<br>".join([f"{d.user_id} - {d.amount} - {d.category}" for d in details])
    






















    