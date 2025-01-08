from models import db, User


def add_user(name, email):
    user = User(name=name, email=email)
    db.session.add(user)
    db.session.commit()


def get_all_users():
    return User.query.all()


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