from flask import Flask, render_template, request, redirect, url_for, flash, session
import importlib

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Defining routes for different functionalities

# Main page route
@app.route('/')
def index():
    # Your main page logic here
    return render_template('login.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Login logic here

    # Importing users from app module
    users = importlib.import_module('app').users
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user_type = request.form['user_type']

        if email == users[user_type]['email'] and password == users[user_type]['password']:
            session['email'] = email
            session['role'] = user_type
            return redirect(url_for(f'{user_type}_dashboard'))
        else:
            flash('Invalid email or password. Please try again.', 'error')
            return redirect(url_for('login'))
    else:
        return render_template('login.html')

# Logout route
@app.route('/logout')
def logout():
    # Logout logic here
    session.clear()
    return redirect(url_for('index'))

# Dashboard route
@app.route('/dashboard')
def dashboard():
    # Dashboard logic here
    if 'email' not in session:
        flash('You need to login first!', 'error')
        return redirect(url_for('login'))
    role = session.get('role')
    if role == 'admin':
        # Admin dashboard logic
        return render_template('admin_dashboard.html')
    elif role == 'student':
        # Student dashboard logic
        return render_template('student_dashboard.html')
    elif role == 'lecturer':
        # Lecturer dashboard logic
        return render_template('lecturer_dashboard.html')
    else:
        flash('Invalid user role!', 'error')
        return redirect(url_for('index'))

# Route for profile editing
@app.route('/profile_edit', methods=['GET', 'POST'])
def profile_edit():
    """Edit user profile."""
    users = importlib.import_module('app').users  # Import users from app module
    if 'email' not in session:
        flash('You need to be logged in to access this page.', 'error')
        return redirect(url_for('login'))

    if request.method == 'POST':
        email = session['email']
        name = request.form['name']
        users[email]['name'] = name
        flash('Profile updated successfully', 'success')
        return redirect(url_for('profile_edit'))
    else:
        user_email = session['email']
        return render_template('profile_edit.html', user=users[user_email])

# Route for registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    # Registration logic here
    if request.method == 'POST':
        # Registration logic
        pass
    else:
        return render_template('register.html')

# Route for student dashboard
@app.route('/student/dashboard')
def student_dashboard():
    """Display the student dashboard."""
    return render_template('student_dashboard.html')

# Route for student projects
@app.route('/student/projects')
def student_projects():
    """Display projects submitted by the student"""
    pass

# Route for supervisor information
@app.route('/student/supervisor')
def supervisor_info():
    """Display assigned supervisor information"""
    pass

# Route for password reset
@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        # Password reset logic
        pass
    else:
        return render_template('reset_password.html')

# Route for project submission
@app.route('/submit_project', methods=['POST'])
def submit_project():
    # Check if the student is logged in
    if 'email' not in session:
        # If not, redirect the student to the login page
        flash('You need to be logged in to access this page.', 'error')
        return redirect(url_for('login'))

    # Retrieve project details from the form
    project_title = request.form['project_title']
    project_description = request.form['project_description']
    project_type = request.form['project_type']
    project_supervisor = request.form['project_supervisor']

    # Add the new project to the list of submitted projects
    submitted_projects[session['email']] = {
        'title': project_title,
        'description': project_description,
        'type': project_type,
        'supervisor': project_supervisor,
        'status': 'pending'
    }

    # Redirect the student to their dashboard
    return redirect(url_for('student.dashboard'))

# Route for notifications
@app.route('/notifications')
def display_notifications():
    user_notifications = session.get('notifications', [])
    return render_template('notifications.html', notifications=user_notifications)

# Route for allocating supervisor
@app.route('/allocate_supervisor', methods=['POST'])
def allocate_supervisor():
    if 'email' not in session or session.get('role') != 'admin':
        # Redirect if user is not logged in as admin
        return redirect(url_for('login'))

    # Get form data
    email = request.form['email']
    supervisor_name = request.form['supervisor_name']

    # Assign supervisor to student
    supervisor_allocation[email] = supervisor_name

    # Redirect to admin dashboard
    return redirect(url_for('dashboard'))

# Add other routes for admin, auth, lecturer, notifications, password reset, projects, registration, student, supervisor, users functionalities here

if __name__ == '__main__':
    app.run(debug=True)
