from flask import Flask, redirect, render_template, request, session
from flask_migrate import Migrate
from models import db
from operations import add_user
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
    """
    Handles user login functionality.

    This endpoint allows users to log in to the application. It supports both
    GET and POST methods. When accessed through GET, the login page is rendered
    and served to the user. When accessed through POST, the method processes
    the login credentials submitted by the user, storing the user's name in
    the session, and redirects to the root page.

    :parameters: None

    :raises KeyError: If the "name" key does not exist in the form data during a
        POST request.

    :return: A rendered login page template on a GET request. On a POST request,
        redirects the user to the root page after successfully setting the session
        variable.
    """
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
    """
    Handles the endpoint for the caloric calculator. This function responds to GET and POST
    requests, processes form input for calculating Basal Metabolic Rate (BMR) and total daily
    energy expenditure, and renders the corresponding results page.

    If the request method is POST, it retrieves user-provided data such as sex, weight, height,
    age, and activity level from the form input. It then calculates the BMR and daily caloric
    needs using imported functions. Finally, it renders the result page with the calculated
    values. For GET requests, it renders the initial form page.

    :raises ValueError: If the form fields for weight, height, or age are improperly formatted
        or cannot be converted to integers.
    :raises TypeError: If the activity level does not match expected input format, as
        `harris_benedict_calculation` may assume a valid pre-defined activity level.
    :returns: If a POST request is made, returns the caloric calculation results and directs
        the user to a page displaying them. If a GET request is made, displays
        the caloric calculator form to the user.
    :rtype: flask.wrappers.Response
    """
    if request.method == "POST":
        gender      =                     str(request.form.get("gender"))
        weight   =                  int(request.form.get("weight"))


        height_ft = int(request.form.get("height_ft"))
        height_in = int(request.form.get("height_in"))

        height = (height_ft * 12) + height_in
        age      =                     int(request.form.get("age"))
        activity =               request.form.get("activity_level")
        # call functions from formulas.py
        bmr      =   basal_metabolic_rate(height, weight, age, gender)
        daily_calories   =       harris_benedict_calculation(activity, bmr)

        return render_template("caloric_results.html", daily_calories=daily_calories)
    return render_template("caloric_calculator_concept_2.html")


@app.route("/meal_plan", methods=["GET"])
def view_meal_plan():

    return render_template("mealplan.html", name=session.get("name"))


@app.route("/meal_plan_new", methods=["GET", "POST"])
def create_meal_plan():
    """
    Creates a new meal plan for the user. This function handles both GET and POST
    methods. For a GET request, it renders the form for creating a new meal plan.
    For a POST request, it retrieves the data submitted by the user via the form,
    processes the data by calling the `create_meal_plan` function, and redirects
    the user to the meal plan page.

    :param user_email: The email or unique identifier of the user, extracted from
        the session.
    :type user_email: str
    :param week_start_date: The start date for the meal plan, extracted from the
        form submission.
    :type week_start_date: str
    :param meal_plan: The meal plan data submitted by the user, extracted from
        the form submission as a JSON string or plain text.
    :type meal_plan: str

    :raises KeyError: Raised when required session keys or form fields are
        missing.
    :raises ValueError: Raised when invalid data is provided from the form
        submission.

    :return: If the request method is GET, it renders and returns the meal plan
        creation template. If the request method is POST, it redirects to the
        meal plan page after successfully creating the meal plan.
    :rtype: Union[str, werkzeug.wrappers.response.Response]
    """
    if request.method == "POST":
        user_email = session.get("name")  # Get user's email or unique identifier
        week_start_date = request.form.get("week_start_date")  # Date input from form
        meal_plan = request.form.get("meal_plan")  # Text input (JSON string or plain text)

        create_meal_plan(user_email, week_start_date, meal_plan)
        return redirect("/meal_plan")
    return render_template("new_meal_plan.html")


if __name__ == '__main__':
    app.run()
