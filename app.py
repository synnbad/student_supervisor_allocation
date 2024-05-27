from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'

users = {
    'student': {'email': 'student@example.com', 'password': 'studentpass', 'name': 'Student Name'},
    'lecturer': {'email': 'lecturer@example.com', 'password': 'lecturerpass', 'name': 'Lecturer Name'},
    'admin': {'email': 'admin@example.com', 'password': 'adminpass', 'name': 'Admin Name'}
}

submitted_projects = {}
supervisor_allocation = {}

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user_type = request.form['user_type']

        if user_type in users and email == users[user_type]['email'] and password == users[user_type]['password']:
            session['email'] = email
            session['role'] = user_type
            return redirect(url_for(f'{user_type}_dashboard'))
        else:
            flash('Invalid email or password. Please try again.', 'error')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('email', None)
    session.pop('role', None)
    return redirect(url_for('index'))

@app.route('/student/dashboard')
def student_dashboard():
    if 'email' not in session or session.get('role') != 'student':
        flash('You need to login first!', 'error')
        return redirect(url_for('login'))
    return render_template('student_dashboard.html')

@app.route('/lecturer/dashboard')
def lecturer_dashboard():
    if 'email' not in session or session.get('role') != 'lecturer':
        flash('You need to login first!', 'error')
        return redirect(url_for('login'))
    return render_template('lecturer_dashboard.html')

@app.route('/admin/dashboard')
def admin_dashboard():
    if 'email' not in session or session.get('role') != 'admin':
        flash('You need to login first!', 'error')
        return redirect(url_for('login'))
    return render_template('admin_dashboard.html')

@app.route('/profile_edit', methods=['GET', 'POST'])
def profile_edit():
    if 'email' not in session:
        return redirect(url_for('login'))

    user_email = session['email']
    user_role = session.get('role')

    if request.method == 'POST':
        users[user_role]['name'] = request.form['name']
        flash('Profile updated successfully', 'success')
        return redirect(url_for('profile_edit'))

    return render_template('profile_edit.html', user=users[user_role])

@app.route('/register', methods=['GET', 'POST'])
def register_view():
    if request.method == 'POST':
        # Handle registration logic here
        pass
    return render_template('register.html')

@app.route('/student/projects')
def student_projects():
    if 'email' not in session or session.get('role') != 'student':
        return redirect(url_for('login'))
    email = session['email']
    return render_template('student_projects.html', projects=submitted_projects.get(email, {}))

@app.route('/student/supervisor')
def supervisor_info():
    if 'email' not in session or session.get('role') != 'student':
        return redirect(url_for('login'))
    email = session['email']
    return render_template('supervisor_info.html', supervisor=supervisor_allocation.get(email, {}))

@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        # Handle password reset logic here
        pass
    return render_template('reset_password.html')

@app.route('/submit_project', methods=['POST'])
def submit_project():
    if 'email' not in session or session.get('role') != 'student':
        flash('You need to be logged in to access this page.', 'error')
        return redirect(url_for('login'))

    project_title = request.form['project_title']
    project_description = request.form['project_description']
    project_type = request.form['project_type']
    project_supervisor = request.form['project_supervisor']

    submitted_projects[session['email']] = {
        'title': project_title,
        'description': project_description,
        'type': project_type,
        'supervisor': project_supervisor,
        'status': 'pending'
    }

    return redirect(url_for('student_dashboard'))

@app.route('/display_notifications')
def display_notifications():
    return render_template('notifications.html')

@app.route('/allocate_supervisor', methods=['POST'])
def allocate_supervisor():
    if 'email' not in session or session.get('role') != 'admin':
        return redirect(url_for('login'))

    email = request.form['email']
    supervisor_name = request.form['supervisor_name']

    supervisor_allocation[email] = supervisor_name

    return redirect(url_for('admin_dashboard'))

# Lecturer additional functionalities
@app.route('/lecturer/assigned_students')
def assigned_students():
    if 'email' not in session or session.get('role') != 'lecturer':
        flash('You need to login first!', 'error')
        return redirect(url_for('login'))
    # Fetch students assigned to this lecturer
    lecturer_email = session['email']
    students = {email: details for email, details in supervisor_allocation.items() if details == lecturer_email}
    return render_template('assigned_students.html', students=students)

@app.route('/lecturer/review_projects')
def review_projects():
    if 'email' not in session or session.get('role') != 'lecturer':
        flash('You need to login first!', 'error')
        return redirect(url_for('login'))
    # Fetch projects submitted to this lecturer
    lecturer_email = session['email']
    projects = {email: project for email, project in submitted_projects.items() if project['supervisor'] == lecturer_email}
    return render_template('review_projects.html', projects=projects)

@app.route('/lecturer/schedule_meeting', methods=['GET', 'POST'])
def schedule_meeting():
    if 'email' not in session or session.get('role') != 'lecturer':
        flash('You need to login first!', 'error')
        return redirect(url_for('login'))
    if request.method == 'POST':
        # Handle meeting scheduling logic here
        flash('Meeting scheduled successfully', 'success')
        return redirect(url_for('schedule_meeting'))
    return render_template('schedule_meeting.html')

# Admin additional functionalities
@app.route('/admin/view_users')
def view_users():
    if 'email' not in session or session.get('role') != 'admin':
        flash('You need to login first!', 'error')
        return redirect(url_for('login'))
    return render_template('view_users.html', users=users)

@app.route('/admin/view_projects')
def view_projects():
    if 'email' not in session or session.get('role') != 'admin':
        flash('You need to login first!', 'error')
        return redirect(url_for('login'))
    return render_template('view_projects.html', projects=submitted_projects)

@app.route('/admin/manage_roles', methods=['GET', 'POST'])
def manage_roles():
    if 'email' not in session or session.get('role') != 'admin':
        flash('You need to login first!', 'error')
        return redirect(url_for('login'))
    if request.method == 'POST':
        email = request.form['email']
        new_role = request.form['role']
        # Update user role logic here
        for role, user in users.items():
            if user['email'] == email:
                user['role'] = new_role
                flash('Role updated successfully', 'success')
                return redirect(url_for('manage_roles'))
        flash('User not found', 'error')
    return render_template('manage_roles.html', users=users)

if __name__ == '__main__':
    app.run(debug=True)
