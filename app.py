import os
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a secure key

# Configuration for file uploads
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'txt'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Sample users data
users = {
    'student': {'email': 'student@example.com', 'password': 'studentpass', 'name': 'Student Name'},
    'lecturer': {'email': 'lecturer@example.com', 'password': 'lecturerpass', 'name': 'Lecturer Name'},
    'admin': {'email': 'admin@example.com', 'password': 'adminpass', 'name': 'Admin Name'}
}

supervisors = {
    1: {'name': 'Dr. Smith', 'email': 'smith@example.com', 'department': 'Computer Science'},
    2: {'name': 'Dr. Jones', 'email': 'jones@example.com', 'department': 'Mathematics'}
}


# Initialize projects and supervisor allocation dictionaries
projects = {}
submitted_projects = {}
supervisor_allocation = {}

# Helper function to check allowed file types
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# MAIN ROUTE
@app.route('/')
def index():
    return render_template('login.html')

# LOGIN ROUTE
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

# LOGOUT ROUTE
@app.route('/logout')
def logout():
    session.pop('email', None)
    session.pop('role', None)
    return redirect(url_for('index'))

# STUDENT DASHBOARD
@app.route('/student/dashboard')
def student_dashboard():
    if 'email' not in session or session.get('role') != 'student':
        flash('You need to login first!', 'error')
        return redirect(url_for('login'))
    return render_template('student_dashboard.html', user=users['student'])

# LECTURER DASHBOARD
@app.route('/lecturer/dashboard')
def lecturer_dashboard():
    if 'email' not in session or session.get('role') != 'lecturer':
        flash('You need to login first!', 'error')
        return redirect(url_for('login'))
    return render_template('lecturer_dashboard.html', user=users['lecturer'])

# ADMIN DASHBOARD
@app.route('/admin/dashboard')
def admin_dashboard():
    if 'email' not in session or session.get('role') != 'admin':
        flash('You need to login first!', 'error')
        return redirect(url_for('login'))
    return render_template('admin_dashboard.html', user=users['admin'])

# ADD PROJECT ROUTE
@app.route('/admin/add_project', methods=['GET', 'POST'])
def add_project():
    if 'email' not in session or session.get('role') != 'admin':
        flash('You need to login first!', 'error')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        new_id = max(projects.keys(), default=0) + 1  # Ensure projects is initialized
        projects[new_id] = {
            'title': request.form['title'],
            'description': request.form['description']
        }
        flash('Project added successfully', 'success')
        return redirect(url_for('manage_projects'))
    return render_template('add_project.html')

# EDIT PROJECT ROUTE
@app.route('/admin/edit_supervisor/<int:supervisor_id>', methods=['GET', 'POST'])
def edit_supervisor(supervisor_id):
    if 'email' not in session or session.get('role') != 'admin':
        flash('You need to login first!', 'error')
        return redirect(url_for('login'))

    # Find the supervisor by id
    supervisor = supervisors.get(supervisor_id)

    if request.method == 'POST':
        # Update supervisor details
        supervisor['name'] = request.form['name']
        supervisor['email'] = request.form['email']
        supervisor['department'] = request.form['department']
        flash('Supervisor updated successfully', 'success')
        return redirect(url_for('manage_supervisors'))

    return render_template('edit_supervisor.html', supervisor=supervisor)

# Example data structure for supervisors
supervisors = {
    1: {'id': 1, 'name': 'Dr. John Doe', 'email': 'john.doe@university.edu', 'department': 'Computer Science'},
    2: {'id': 2, 'name': 'Dr. Jane Smith', 'email': 'jane.smith@university.edu', 'department': 'Mathematics'}
}
# DELETE PROJECT ROUTE
@app.route('/admin/delete_project/<int:project_id>')
def delete_project(project_id):
    if 'email' not in session or session.get('role') != 'admin':
        flash('You need to login first!', 'error')
        return redirect(url_for('login'))
    
    if project_id in projects:
        del projects[project_id]
        flash('Project deleted successfully', 'success')
    else:
        flash('Project not found', 'error')
    return redirect(url_for('manage_projects'))

# MANAGE SUPERVISORS ROUTE
@app.route('/admin/manage_supervisors')
def manage_supervisors():
    if 'email' not in session or session.get('role') != 'admin':
        flash('You need to login first!', 'error')
        return redirect(url_for('login'))
    
    return render_template('manage_supervisors.html', supervisors=supervisors)


# PROFILE EDIT ROUTE
@app.route('/profile_edit', methods=['GET', 'POST'])
def profile_edit():
    if 'email' not in session:
        flash('You need to login first!', 'error')
        return redirect(url_for('login'))

    user_role = session.get('role')
    if request.method == 'POST':
        users[user_role]['name'] = request.form['name']
        flash('Profile updated successfully', 'success')
        return redirect(url_for('profile_edit'))
    return render_template('profile_edit.html', user=users[user_role])

# REGISTER ROUTE
@app.route('/register', methods=['GET', 'POST'])
def register_view():
    if request.method == 'POST':
        # Handle registration logic here
        pass
    return render_template('register.html')

# STUDENT PROJECTS ROUTE
@app.route('/student/projects')
def student_projects():
    if 'email' not in session or session.get('role') != 'student':
        flash('You need to login first!', 'error')
        return redirect(url_for('login'))
    email = session['email']
    return render_template('student_projects.html', projects=submitted_projects.get(email, {}))

# SUPERVISOR INFO ROUTE
@app.route('/student/supervisor')
def supervisor_info():
    if 'email' not in session or session.get('role') != 'student':
        flash('You need to login first!', 'error')
        return redirect(url_for('login'))
    email = session['email']
    supervisor = supervisor_allocation.get(email, None)
    return render_template('supervisor_info.html', supervisor=supervisor)

# RESET PASSWORD ROUTE
@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        # Handle password reset logic here
        pass
    return render_template('reset_password.html')

# SUBMIT PROJECT ROUTE
@app.route('/submit_project', methods=['POST'])
def submit_project():
    if 'email' not in session or session.get('role') != 'student':
        flash('You need to be logged in to access this page.', 'error')
        return redirect(url_for('login'))

    if 'project_file' not in request.files:
        flash('No file part', 'error')
        return redirect(url_for('student_projects'))

    file = request.files['project_file']
    if file.filename == '':
        flash('No selected file', 'error')
        return redirect(url_for('student_projects'))

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        project_title = request.form['project_title']
        project_description = request.form['project_description']
        project_type = request.form['project_type']
        project_supervisor = request.form['project_supervisor']

        submitted_projects[session['email']] = {
            'title': project_title,
            'description': project_description,
            'type': project_type,
            'supervisor': project_supervisor,
            'status': 'pending',
            'file_path': os.path.join(app.config['UPLOAD_FOLDER'], filename)
        }

        flash('Project submitted successfully', 'success')
        return redirect(url_for('student_dashboard'))

    flash('Invalid file type', 'error')
    return redirect(url_for('student_projects'))

# DISPLAY NOTIFICATIONS ROUTE
@app.route('/display_notifications')
def display_notifications():
    return render_template('notifications.html')

# ALLOCATE SUPERVISOR ROUTE
@app.route('/allocate_supervisor', methods=['POST'])
def allocate_supervisor():
    if 'email' not in session or session.get('role') != 'admin':
        flash('You need to login first!', 'error')
        return redirect(url_for('login'))

    email = request.form['email']
    supervisor_name = request.form['supervisor_name']
    supervisor_allocation[email] = supervisor_name

    flash('Supervisor allocated successfully', 'success')
    return redirect(url_for('admin_dashboard'))

# LECTURER ASSIGNED STUDENTS ROUTE
@app.route('/lecturer/assigned_students', methods=['GET', 'POST'])
def assigned_students():
    if 'email' not in session or session.get('role') != 'lecturer':
        flash('You need to login first!', 'error')
        return redirect(url_for('login'))

    lecturer_email = session['email']

    if request.method == 'POST':
        student_email = request.form['student_email']
        supervisor_allocation[student_email] = lecturer_email
        flash('Student assigned successfully', 'success')

    # Fetch students assigned to this lecturer
    students = {email: details for email, details in supervisor_allocation.items() if details == lecturer_email}
    student_names = {email: users['student']['name'] for email in students}

    return render_template('assigned_students.html', students=student_names, lecturer_email=lecturer_email)

# UNASSIGN STUDENT ROUTE
@app.route('/lecturer/unassign_student', methods=['POST'])
def unassign_student():
    if 'email' not in session or session.get('role') != 'lecturer':
        flash('You need to login first!', 'error')
        return redirect(url_for('login'))

    student_email = request.form['student_email']
    lecturer_email = session['email']

    if supervisor_allocation.get(student_email) == lecturer_email:
        del supervisor_allocation[student_email]
        flash('Student unassigned successfully', 'success')
    else:
        flash('Failed to unassign student', 'error')

    return redirect(url_for('assigned_students'))

# LECTURER REVIEW PROJECTS ROUTE
@app.route('/lecturer/review_projects')
def review_projects():
    if 'email' not in session or session.get('role') != 'lecturer':
        flash('You need to login first!', 'error')
        return redirect(url_for('login'))
    
    lecturer_email = session['email']
    projects = {email: project for email, project in submitted_projects.items() if project['supervisor'] == lecturer_email}
    return render_template('review_projects.html', projects=projects)

# APPROVE PROJECT ROUTE
@app.route('/approve_project', methods=['POST'])
def approve_project():
    if 'email' not in session or session.get('role') != 'lecturer':
        flash('You need to login first!', 'error')
        return redirect(url_for('login'))
    
    student_email = request.form['student_email']
    # Implement the logic to approve the project
    flash(f'Project from {student_email} approved.', 'success')
    return redirect(url_for('review_projects'))

# REJECT PROJECT ROUTE
@app.route('/reject_project', methods=['POST'])
def reject_project():
    if 'email' not in session or session.get('role') != 'lecturer':
        flash('You need to login first!', 'error')
        return redirect(url_for('login'))
    
    student_email = request.form['student_email']
    # Implement the logic to reject the project
    flash(f'Project from {student_email} rejected.', 'success')
    return redirect(url_for('review_projects'))

# LECTURER SCHEDULE MEETING ROUTE
@app.route('/lecturer/schedule_meeting', methods=['GET', 'POST'])
def schedule_meeting():
    if 'email' not in session or session.get('role') != 'lecturer':
        flash('You need to login first!', 'error')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        student_email = request.form['student_email']
        date = request.form['date']
        time = request.form['time']
        description = request.form['description']

        # Add the meeting to the meetings list
        meetings.append({
            'lecturer': session['email'],
            'student': student_email,
            'date': date,
            'time': time,
            'description': description
        })

        flash('Meeting scheduled successfully', 'success')
        return redirect(url_for('schedule_meeting'))
    return render_template('schedule_meeting.html')

# ADMIN VIEW USERS ROUTE
@app.route('/admin/view_users')
def view_users():
    if 'email' not in session or session.get('role') != 'admin':
        flash('You need to login first!', 'error')
        return redirect(url_for('login'))
    
    # Assuming you have a dictionary 'users' containing user data
    all_users = users  # Or fetch from your database
    return render_template('view_users.html', users=all_users)

# ADMIN MANAGE PROJECTS ROUTE
@app.route('/admin/manage_projects')
def manage_projects():
    if 'email' not in session or session.get('role') != 'admin':
        flash('You need to login first!', 'error')
        return redirect(url_for('login'))
    
    return render_template('manage_projects.html', projects=projects)



# ADD SUPERVISOR ROUTE
@app.route('/admin/add_supervisor', methods=['GET', 'POST'])
def add_supervisor():
    if 'email' not in session or session.get('role') != 'admin':
        flash('You need to login first!', 'error')
        return redirect(url_for('login'))

    if request.method == 'POST':
        new_id = max(supervisors.keys(), default=0) + 1
        supervisors[new_id] = {
            'name': request.form['name'],
            'email': request.form['email'],
            'department': request.form['department']
        }
        flash('Supervisor added successfully', 'success')
        return redirect(url_for('manage_supervisors'))
    return render_template('add_supervisor.html')



# DELETE SUPERVISOR ROUTE
@app.route('/admin/delete_supervisor/<int:supervisor_id>')
def delete_supervisor(supervisor_id):
    if 'email' not in session or session.get('role') != 'admin':
        flash('You need to login first!', 'error')
        return redirect(url_for('login'))

    if supervisor_id in supervisors:
        del supervisors[supervisor_id]
        flash('Supervisor deleted successfully', 'success')
    else:
        flash('Supervisor not found', 'error')
    return redirect(url_for('manage_supervisors'))


if __name__ == '__main__':
    app.run(debug=True)
