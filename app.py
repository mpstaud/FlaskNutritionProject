from crypt import methods

from flask import Flask, redirect, render_template, request, session
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from models import db, User, FoodLog, MealPlan
from operations import add_user, get_all_users, add_food_log
from flask_session import Session
from formulas import basal_metabolic_rate, harris_benedict_calculation

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'  # Database file name
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable event system for performance

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db.init_app(app)
migrate = Migrate(app, db)


@app.route('/')
def index():  # put application's code here
    with app.app_context():
        user = add_user('Matt', 'staudachermatthew@gmail.com')
        print(user)
    '''
    with app.app_context():
        log = add_food_log(
            user_email='staudachermatthew@gmail.com',
            food_item='Banana',
            calories=105
        )
        print(log)
    '''
    return render_template("index.html", name=session.get("name"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        session["name"] = request.form.get("name")
        return redirect("/")
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/caloric_calculator", methods=["GET", "POST"])
def caloric_calculator():
    if request.method == "POST":
        sex = str(request.form.get("sex"))
        weight = int(request.form.get("weight"))
        height = int(request.form.get("height"))
        age = int(request.form.get("age"))
        activity = request.form.get("activity_level")
        bmr = basal_metabolic_rate(height, weight, age, sex)
        result = harris_benedict_calculation(activity, bmr)
        return render_template("caloric_results.html", result=result)
    return render_template("caloric_calculator.html")


@app.route("/meal_plan", methods=["GET"])
def view_meal_plan():
    return "<p>Meal plan</p>"


@app.route("/meal_plan_new", methods=["GET", "POST"])
def create_meal_plan():
    if request.method == "POST":
        user_email = session.get("name")  # Get user's email or unique identifier
        week_start_date = request.form.get("week_start_date")  # Date input from form
        meal_plan = request.form.get("meal_plan")  # Text input (JSON string or plain text)

        create_meal_plan(user_email, week_start_date, meal_plan)
        return redirect("/meal_plan")
    return render_template("new_meal_plan.html")


if __name__ == '__main__':
    app.run()
