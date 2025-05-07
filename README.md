# 💸 Flask Expense Tracker App

A personal finance tracking web app built using **Flask**, with CRUD functionality, search/filter features, and a dashboard for data visualization using **Pygal**.

---

## 📚 What I Learned

- Flask fundamentals: routing, templates, and app factory pattern.
- SQLAlchemy ORM for database operations.
- Handling forms with GET and POST requests.
- Filtering database results using `ilike`, `or_`, and `cast`.
- Creating visual dashboards with **Pygal** (Pie and Bar charts).
- Performing CRUD operations: Create, Read, Update, Delete.

---

## 🛠 What I Used

- Python
- Flask
- SQLAlchemy
- SQLite
- Pygal
- Jinja2 templating engine
- Standard Python libraries (`datetime`, `os`)

---

## ✅ What Was Done Well

- Used application factory pattern (`create_app()`).
- Organized code with a single model and clean route definitions.
- Implemented full CRUD operations with SQLAlchemy.
- Built a dynamic dashboard using Pygal charts.
- Used clear, readable code with helpful comments.
- Search/filter functionality using SQLAlchemy queries.

---

## 🧪 What Should Be Improved

- Add input validation and error handling for forms.
- Use environment variables for sensitive data (like `secret_key`).
- Implement CSRF protection (e.g., using Flask-WTF).
- Add flash messages for user feedback.
- Refactor app into **Blueprints** for better scalability.
- Use form libraries for better UX and cleaner server-side logic.

---

## 🚀 How the App Works

1. **Home Page (`/`)**: Landing page.
2. **Add Expense (`/manage-expense`)**: Users submit new expenses via a form.
3. **View & Filter (`/manage-expense/view`)**: All entries shown, with search/filter options.
4. **Update (`/manage-expense/update/<id>`)**: Users can edit any expense.
5. **Delete (`/manage-expense/delete/<id>`)**: Users can delete an expense after confirmation.
6. **Dashboard (`/dashboard`)**: Visual summaries (pie chart + bar chart) showing category-wise spending.

---

## 📁 Project Structure (Basic Overview)

main test codes/
├── run.py
└── app/
    ├── __init__.py
    ├── routes.py
    ├── models.py
    ├── app.db
    └── templates/
        ├── base.html
        ├── dashboard.html
        ├── delete.html
        ├── filter.html
        ├── home.html
        ├── update.html
        └── view.html

---

## 🧠 Author Notes

This is my first full Flask app. I started with **zero experience in Flask**, learned from tutorials and documentation, and built this by combining knowledge from various sources. I'm proud of this milestone and looking forward to improving and scaling this further!

