from flask import render_template, request, redirect, url_for, flash, session
from app import app, users, supervisor_allocation, submitted_projects, project_reviews
from app import generate_supervisor_notification, generate_project_approval_notification
from werkzeug.exceptions import abort

# Sample user data (replace with database interactions)
users = {
    'student': {'email': 'student@example.com', 'password': 'studentpassword'},
    'lecturer': {'email': 'lecturer@example.com', 'password': 'lecturerpassword'},
    'admin': {'email': 'admin@example.com', 'password': 'adminpassword'}
}

@app.route('/')
def index():
    return "Welcome to the Student Supervisor Allocation System!"

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user_type = request.form['user_type']

        if email == users[user_type]['email'] and password == users[user_type]['password']:
            # Redirect users to different dashboards based on user type
            if user_type == 'student':
                return redirect(url_for('student_dashboard'))
            elif user_type == 'lecturer':
                return redirect(url_for('lecturer_dashboard'))
            elif user_type == 'admin':
                return redirect(url_for('admin_dashboard'))
        else:
            return "Invalid email or password. Please try again."
    else:
        return render_template('login.html')


@app.route('/student_dashboard')
def student_dashboard():
    # Check if the user is logged in as a student
    if 'email' not in session or session['role'] != 'student':
        # If not logged in or not a student, redirect to the login page
        return redirect(url_for('login'))

    # Get the email of the logged-in student
    student_email = session['email']

    # Get the projects submitted by the current student
    student_projects = submitted_projects.get(student_email, [])

    # Render the student dashboard template with the student's projects
    return render_template('student_dashboard.html', projects=student_projects)

@app.route('/lecturer_dashboard')
def lecturer_dashboard():
    # Check if the user is logged in as a lecturer
    if 'email' not in session or session['role'] != 'lecturer':
        # If not logged in or not a lecturer, redirect to the login page
        return redirect(url_for('login'))

    # Get the email of the logged-in lecturer
    lecturer_email = session['email']

    # Get the students allocated to the current lecturer
    allocated_students = {student_email: project_title for student_email, project_title in supervisor_allocation.items() if project_title == lecturer_email}

    # Get the projects submitted by the students allocated to the lecturer
    lecturer_projects = {student_email: submitted_projects.get(student_email) for student_email in allocated_students}

    # Render the lecturer dashboard template with the allocated students and their projects
    return render_template('lecturer_dashboard.html', students=allocated_students, projects=lecturer_projects)

@app.route('/admin_dashboard')
def admin_dashboard():
    # Check if the user is logged in as an admin
    if 'email' not in session or session['role'] != 'admin':
        # If not logged in or not an admin, redirect to the login page
        return redirect(url_for('login'))

    # Get all allocated students and their supervisors
    allocated_students = {student_email: supervisor for student_email, supervisor in supervisor_allocation.items()}

    # Get all submitted projects
    all_projects = submitted_projects

    # Render the admin dashboard template with allocated students and all projects
    return render_template('admin_dashboard.html', students=allocated_students, projects=all_projects)

@app.route('/notifications')
def notifications():
    # Get notifications for the logged-in user
    user_email = session.get('email')  # Assuming the user's email is stored in the session
    user_notifications = users.get(user_email, {}).get('notifications', [])
    return render_template('notifications.html', notifications=user_notifications)

@app.route('/allocate_supervisor', methods=['POST'])
def allocate_supervisor():
    # Check if the user is logged in as an admin
    if 'email' not in session or session['role'] != 'admin':
        # If not logged in or not an admin, redirect to the login page
        flash('You are not authorized to perform this action.', 'error')
        return redirect(url_for('login'))

    # Get the form data submitted by the user
    student_email = request.form.get('student_email')
    supervisor_name = request.form.get('supervisor_name')

    # Update the supervisor allocation data
    supervisor_allocation[student_email] = supervisor_name

    # Generate a notification for the student
    generate_supervisor_notification(student_email, supervisor_name)

    # Flash a success message
    flash('Supervisor allocated successfully', 'success')

    # Redirect to the admin dashboard
    return redirect(url_for('admin_dashboard'))
@app.route('/approve_project', methods=['POST'])


@app.route('/approve_project', methods=['POST'])
def approve_project():
    # Check if the user is logged in as an admin
    if 'email' not in session or session['role'] != 'admin':
        # If not logged in or not an admin, redirect to the login page
        flash('You are not authorized to perform this action.', 'error')
        return redirect(url_for('login'))

    # Get the form data submitted by the user
    student_email = request.form.get('student_email')
    project_title = request.form.get('project_title')

    # Update the project status to approved
    submitted_projects[student_email] = project_title

    # Generate a notification for the student
    generate_project_approval_notification(student_email, project_title, 'approved')

    # Flash a success message
    flash('Project approved successfully', 'success')

    # Redirect to the admin dashboard
    return redirect(url_for('admin_dashboard'))

@app.route('/reject_project', methods=['POST'])
def reject_project():
    # Check if the user is logged in as an admin
    if 'email' not in session or session['role'] != 'admin':
        # If not logged in or not an admin, redirect to the login page
        flash('You are not authorized to perform this action.', 'error')
        return redirect(url_for('login'))

    # Get the form data submitted by the user
    student_email = request.form.get('student_email')
    project_title = request.form.get('project_title')

    # Update the project status to rejected
    submitted_projects[student_email] = project_title

    # Generate a notification for the student
    generate_project_approval_notification(student_email, project_title, 'rejected')

    # Flash a success message
    flash('Project rejected successfully', 'success')

    # Redirect to the admin dashboard
    return redirect(url_for('admin_dashboard'))

@app.route('/search_project', methods=['GET'])
def search_project():
    # Get the search query from the request
    query = request.args.get('query', '')

    # Perform the search
    results = {}
    for student_email, project_title in submitted_projects.items():
        if query.lower() in project_title.lower():
            results[student_email] = project_title

    # Render the search results template
    return render_template('search_results.html', query=query, results=results)


@app.route('/project_details/<title>')
def project_details(title):
    # Check if the project exists in the project_details dictionary
    if title not in project_details:
        abort(404)  # Project not found, return 404 error
    
    # Get the project details
    details = project_details[title]
    
    # Get existing reviews and ratings for the project
    reviews_data = project_reviews.get(title, {'reviews': [], 'ratings': []})
    
    # Render the project details template
    return render_template('project_details.html', project_details=details, project_reviews=reviews_data)

@app.route('/profile_edit', methods=['GET', 'POST'])
def profile_edit():
    if request.method == 'POST':
        email = request.form['email']
        name = request.form['name']
        # Update user's profile (you can replace this with your actual logic)
        users[email]['name'] = name
        flash('Profile updated successfully', 'success')
        return redirect(url_for('profile_edit'))
    else:
        # Render profile editing form
        return render_template('profile_edit.html', user=users['student'])  # Assuming the user is a student

@app.route('/reset_password', methods=['POST'])
def reset_password():
    if request.method == 'POST':
        current_password = request.form['current_password']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']
        # Check if current password matches (you can replace this with your actual logic)
        if current_password == users['student']['password']:
            # Check if new password and confirm password match
            if new_password == confirm_password:
                # Update user's password
                users['student']['password'] = new_password
                flash('Password reset successfully', 'success')
                return redirect(url_for('reset_password'))
            else:
                flash('New password and confirm password do not match', 'error')
                return redirect(url_for('reset_password'))
        else:
            flash('Incorrect current password', 'error')
            return redirect(url_for('reset_password'))

@app.route('/delete_account', methods=['POST'])
def delete_account():
    if request.method == 'POST':
        # Delete user's account (you can replace this with your actual logic)
        del users['student']
        flash('Your account has been deleted', 'success')
        return redirect(url_for('index'))

@app.route('/submit_review', methods=['POST'])
def submit_review():
    # Review submission logic (already implemented)

    # Get data from the form submission
    project_title = request.form.get('project_title')
    review = request.form.get('review')
    rating = int(request.form.get('rating'))  # Convert rating to integer
     
    # Update project reviews and ratings
    if project_title in project_reviews:
        project_reviews[project_title]['reviews'].append(review)
        project_reviews[project_title]['ratings'].append(rating)
        flash('Review submitted successfully', 'success')
    else:
        flash('Project not found', 'error')
    
    # Redirect to the project details page
    return redirect(url_for('project_details', title=project_title))
