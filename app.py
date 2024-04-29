from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # Example SQLite database URI
db = SQLAlchemy(app)

# Import route definitions from routes.py
from routes import *

if __name__ == '__main__':
    app.run(debug=True)
