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
meetings = []

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

fields_of_interest = [
    'Computer Science',
    'Mathematics',
    'Physics',
    'Biology',
    'Chemistry',
    'Engineering'
]

@app.route('/select_fields', methods=['GET', 'POST'])
def select_fields():
    if 'email' not in session or session.get('role') != 'student':
        flash('You need to login first!', 'error')
        return redirect(url_for('login'))

    if request.method == 'POST':
        selected_fields = request.form.getlist('fields')
        if len(selected_fields) != 3:
            flash('You must select exactly three fields of interest.', 'error')
            return redirect(url_for('select_fields'))

        # Save the student's field selections
        email = session['email']
        submitted_projects[email] = {
            'fields_of_interest': selected_fields
        }

        flash('Fields of interest submitted successfully.', 'success')
        return redirect(url_for('student_dashboard'))

    return render_template('select_fields.html', fields=fields_of_interest)

# LECTURER DASHBOARD
@app.route('/lecturer/dashboard')
def lecturer_dashboard():
    if 'email' not in session or session.get('role') != 'lecturer':
        flash('You need to login first!', 'error')
        return redirect(url_for('login'))
    return render_template('lecturer_dashboard.html', user=users['lecturer'])

@app.route('/lecturer/projects')
def lecturer_projects():
    # Add logic to retrieve and display lecturer's projects
    return render_template('lecturer_projects.html')

# ADMIN DASHBOARD
@app.route('/admin/dashboard')
def admin_dashboard():
    if 'email' not in session or session.get('role') != 'admin':
        flash('You need to login first!', 'error')
        return redirect(url_for('login'))
    return render_template('admin_dashboard.html', user=users['admin'])

@app.route('/lecturer/select_students', methods=['GET', 'POST'])
def lecturer_select_students():
    if 'email' not in session or session.get('role') != 'lecturer':
        flash('You need to login first!', 'error')
        return redirect(url_for('login'))

    lecturer_email = session['email']
    lecturer_fields = [field for field, lecturer in supervisors.items() if lecturer['email'] == lecturer_email]

    students_for_lecturer = {email: details for email, details in submitted_projects.items() if any(field in lecturer_fields for field in details['fields_of_interest'])}

    if request.method == 'POST':
        student_email = request.form['student_email']
        supervisor_allocation[student_email] = lecturer_email
        flash('Student assigned successfully.', 'success')

    return render_template('lecturer_select_students.html', students=students_for_lecturer)

@app.route('/view_all_students')
def view_all_students():
    if 'email' not in session:
        flash('You need to login first!', 'error')
        return redirect(url_for('login'))

    return render_template('view_all_students.html', students=submitted_projects, supervisors=supervisor_allocation)

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

# MANAGE PROJECTS ROUTE
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
@app.route('/admin/delete_supervisor/<int:supervisor_id>', methods=['POST'])
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

@app.route('/admin/view_users')
def view_users():
    if 'email' not in session or session.get('role') != 'admin':
        flash('You need to login first!', 'error')
        return redirect(url_for('login'))
    
    # Add logic to fetch and display users
    users = users()
    return render_template('view_users.html', users=users)



# EDIT SUPERVISOR ROUTE
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

    email = request.form['student_email']
    supervisor_id = int(request.form['supervisor_id'])

    if email in submitted_projects:
        supervisor_allocation[email] = supervisors[supervisor_id]
        flash(f'Supervisor allocated to {email}', 'success')
    else:
        flash('Invalid student email', 'error')
    return redirect(url_for('admin_dashboard'))

# ADD MEETING ROUTE
@app.route('/add_meeting', methods=['GET', 'POST'])
def add_meeting():
    if 'email' not in session or session.get('role') != 'student':
        flash('You need to login first!', 'error')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        meeting = {
            'title': request.form['title'],
            'description': request.form['description'],
            'date': request.form['date']
        }
        meetings.append(meeting)
        flash('Meeting added successfully', 'success')
        return redirect(url_for('view_meetings'))
    
    return render_template('add_meeting.html')

# VIEW MEETINGS ROUTE
@app.route('/view_meetings')
def view_meetings():
    if 'email' not in session or session.get('role') != 'student':
        flash('You need to login first!', 'error')
        return redirect(url_for('login'))
    
    return render_template('view_meetings.html', meetings=meetings)

if __name__ == '__main__':
    app.run(debug=True)
