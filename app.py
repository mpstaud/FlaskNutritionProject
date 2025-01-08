from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models import db, User
from operations import add_user, get_all_users

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'  # Database file name
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable event system for performance

db.init_app(app)

@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
