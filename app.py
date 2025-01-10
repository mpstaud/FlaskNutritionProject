from flask import Flask, render_template, request
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from models import db, User, FoodLog
from operations import add_user, get_all_users, add_food_log

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'  # Database file name
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable event system for performance

db.init_app(app)
migrate = Migrate(app, db)

@app.route('/',methods=["GET","POST"])
def home():  # put application's code here
    with app.app_context():
        user = add_user('Matt', 'staudachermatthew@gmail.com')
        print(user)
    with app.app_context():
        log = add_food_log(
            user_email='staudachermatthew@gmail.com',
            food_item='Banana',
            calories=105
        )
        print(log)
    if request.method == "POST":
        return render_template("greet.html", name=request.form.get("name"))
    return render_template('index.html')

@app.route("/greet", methods=["post"])
def greet():
    return render_template("greet.html", name=request.args.get("name", "world"))


if __name__ == '__main__':
    app.run()
