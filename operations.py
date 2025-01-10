from models import db, User, FoodLog
from datetime import date
from flask import session

def add_user(name, email):

        # Check if the user already exists
    existing_user = User.query.filter_by(email=email).first()

    if existing_user:
        return existing_user  # Return the existing record if user exists

        # Create a new user
    new_user = User(name=name, email=email)
    db.session.add(new_user)
    db.session.commit()  # Save to the database
    return new_user


def get_all_users():
    return User.query.all()

def get_current_user():
    if 'user_id' not in session:
        raise ValueError("No user is currently logged in!")

    # Query the database to get the user
    user = User.query.get(session['user_id'])
    if not user:
        raise ValueError("User not found in the database!")
    return user


def update_user_email(user_id, new_email):
    user = User.query.get(user_id)
    if user:
        user.email = new_email
        db.session.commit()
        return user
    return None


def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()



def add_food_log(user_email, food_item, calories, log_date=None):
    # Find the user by email (ensure the user exists)
    user = User.query.filter_by(email=user_email).first()
    if not user:
        raise ValueError("No user found with the given email!")

    # Use today's date if no date is provided
    if log_date is None:
        log_date = date.today()

    # Create a new food log entry
    food_log = FoodLog(
        food_item=food_item,
        calories=calories,
        log_date=log_date,
        user_id=user.id  # Associate with the user via foreign key
    )

    # Add to the session and commit
    db.session.add(food_log)
    db.session.commit()
    return food_log