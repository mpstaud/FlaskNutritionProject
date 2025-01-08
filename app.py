from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models import db, User

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'  # Database file name
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable event system for performance

db.init_app(app)

# Create the database (run this only the first time)
with app.app_context():
    db.create_all()
    print("Database and tables created!")
@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
