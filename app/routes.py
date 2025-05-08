from flask import redirect, url_for, render_template, request, session
from app import db
from app.models import Details
from datetime import datetime
from sqlalchemy import or_, cast, String, func
import pygal 

def setup_routes(app):
	@app.route('/')
	def home():
		return render_template('home.html')  # Add this file to templates

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

		categories, totals = zip(*results)  # separate tuples

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
	






















	