# app.py

from flask import Flask
from auth import auth_bp
from student import student_bp
from lecturer import lecturer_bp
from admin import admin_bp
from projects import project_bp
from notifications import notifications_bp

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(student_bp)
app.register_blueprint(lecturer_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(project_bp)
app.register_blueprint(notifications_bp)

if __name__ == '__main__':
    app.run(debug=True)
