from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    age = db.Column(db.Integer, nullable=True)
    food_logs = db.relationship('FoodLog', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.name}>'


class FoodLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Primary key
    food_item = db.Column(db.String(120), nullable=False)
    calories = db.Column(db.Integer, nullable=False)
    log_date = db.Column(db.Date, nullable=False)

    # Foreign key referencing the User table
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"<FoodLog {self.food_item}, {self.calories} calories>"


class MealPlan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String(120), db.ForeignKey('user.email'), nullable=False)
    week_start_date = db.Column(db.Date, nullable=False)  # To track the start week
    meal_plan = db.Column(db.JSON, nullable=False)  # Use JSON or text for flexibility