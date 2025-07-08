from flask import redirect, url_for, render_template, request, session
from app import db, login_manager
from app.models import Details, User
from datetime import datetime
from sqlalchemy import or_, cast, String, func
import pygal 
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user

def setup_routes(app):
	@app.route('/')
	def home():
		return render_template('home.html')  # Add this file to templates

		''' authentication system '''
	@app.route("/signin", methods=["GET", "POST"])
    def signin():
        form = SignInForm()
        
        if form.validate_on_submit():
            username = form.username.data
            password_txt = form.password.data 
            email = form.email.data

            existing_user = User.query.filter_by(email=email).first()

            if existing_user:
                return redirect(url_for('login'))
            else:
                hashed_pw = generate_password_hash(password_txt)

                new_user_entry = User(username=username, email=email, password=hashed_pw)
                
                try:
                    db.session.add(new_user_entry)
                    db.session.commit()
                    
                except SQLAlchemyError as e:
                    db.session.rollback()

                return redirect(url_for('login'))
        
        else:
            return render_template('signin.html', form=form)

    @app.route('/login', methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            email = form.email.data
            password_txt = form.password.data

            verify_user = User.query.filter_by(email=email).first()

            if verify_user and check_password_hash(verify_user.password, password_txt):
                login_user(verify_user)
                return(redirect(url_for('dashboard')))
            else:
                return render_template('login.html', form=form)
                
        else:
            return render_template('login.html', form=form)

	# Data entry in the system
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

		# filtering data + option to update and delete
	@app.route('/manage-expense/view', methods=["POST", "GET"])
	def filter_data():
		if request.method == "POST":
			user_input = request.form.get("fil_data", "").strip() # Safely get and clean user input by removing extra spaces
			search_term = f"%{user_input}%"
	
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

		all_details = Details.query.all() # by default get. 
		return render_template("filter.html", details=all_details)

		# updating data
	@app.route("/manage-expense/update/<int:id>", methods=["POST", "GET"])
	def update_data(id):
		user_to_update = Details.query.get_or_404(id)
		if request.method == "POST":
			user_to_update.amount = request.form['amount']
			user_to_update.description = request.form['description']
			user_to_update.category = request.form['category']
			db.session.commit()
			all_details = Details.query.all()
			return render_template("filter.html", details=all_details)
		else:
			return render_template("update.html", id=id, user=user_to_update)

		# deleting data
	@app.route("/manage-expense/delete/<int:id>", methods=["POST", "GET"])
	def delete_data(id):
		user_to_delete = Details.query.get_or_404(id)
		if request.method == "POST":
			del_confirm = request.form["delete_confirm"]
			if del_confirm.lower() == 'delete':
				db.session.delete(user_to_delete)
				db.session.commit()
				return render_template("filter.html")
		else:
			return render_template("delete.html", id=id, user=user_to_delete)

		# dashboard with graph and table of all data in db
	@app.route("/dashboard")
	def dashboard():
		results = db.session.query(
				Details.category,		# filters data from  amount by category and sums them
				func.sum(Details.amount)
			).group_by(Details.category).all()

		if results:
		    categories, totals = zip(*results)
		else:
		    categories, totals = [], []

		# pie chart
		pie_chart = pygal.Pie(inner_radius=.55)
		pie_chart.title = 'Amount spent on different category'

		for category, total in zip(categories, totals):
			pie_chart.add(category, total)

		chart_data = pie_chart.render_data_uri()  # this gives a data URI instead of a file
		
		# bar chart
		bar_chart = pygal.Bar()
		bar_chart.title = "Comparison of spending"

		for category, total in zip(categories, totals):
			bar_chart.add(category, total)

		chart_data_bar = bar_chart.render_data_uri()

		# importing data for table
		all_details = Details.query.all()


		return render_template(
			    'dashboard.html',
			    chart_data=chart_data,
			    chart_data_bar=chart_data_bar,
			    details=all_details
			)


	# Testing
	# @app.route("/test")
	# def test():
	#     return render_template('update.html')

	# @app.route('/debug-2955')
	# def debug_db():
	#     details = Details.query.all()
	#     return "<br>".join([f"{d.user_id} - {d.amount} - {d.category}" for d in details])
	






















	