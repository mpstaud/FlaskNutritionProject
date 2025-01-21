from models import db, User, FoodLog
from datetime import date
from flask import session

def add_user(name, email):
    """
    Adds a new user to the database or retrieves an existing user given the email.
    It first checks whether a user with the specified email already exists in the
    database. If the user exists, it simply returns the existing user record.
    Otherwise, it creates a new user with the provided name and email and saves
    this record to the database.

    :param name: The name of the user to be added or retrieved.
    :type name: str
    :param email: The email of the user. Used to check if the user already exists.
    :type email: str
    :return: The user object retrieved from the database or the newly created one.
    :rtype: User
    """
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
    """
    Fetches the currently logged-in user from the session. Ensures that a user is logged
    in by checking the presence of 'user_id' in the session, then retrieves the user
    from the database using the stored user ID. Raises errors if no user is logged in
    or if the user is not found in the database.

    :raises ValueError: If there is no user currently logged in or the user is not
        found in the database.
    :returns: The currently logged-in user.

    :rtype: User
    """
    if 'user_id' not in session:
        raise ValueError("No user is currently logged in!")

    # Query the database to get the user
    user = User.query.get(session['user_id'])
    if not user:
        raise ValueError("User not found in the database!")
    return user


def update_user_email(user_id, new_email):
    """
    Updates the email address of a user in the database based on the provided
    user ID. If the user is found, their email is updated with the new email
    address, and the changes are committed to the database. Returns the updated
    user object if the operation is successful or None if the user is not found.

    :param user_id: The unique identifier of the user whose email is to be
        updated.
    :type user_id: int
    :param new_email: The new email address to assign to the user.
    :type new_email: str
    :return: The User object with the updated email address if the user is found,
        otherwise None.
    :rtype: Optional[User]
    """
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

# operations.py

from models import db, MealPlan


def create_meal_plan(user_email, week_start_date, meal_plan):
    """
    Function to create and save a new meal plan in the database.
    """
    if not user_email or not week_start_date or not meal_plan:
        raise ValueError("All fields are required to create a meal plan.")

    # Create a new instance of the MealPlan model
    new_meal_plan = MealPlan(
        user_email=user_email,
        week_start_date=week_start_date,
        meal_plan=meal_plan
    )

    # Add it to the session and commit it
    db.session.add(new_meal_plan)
    db.session.commit()

    return new_meal_plan