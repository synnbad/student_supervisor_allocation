from flask import render_template, request, redirect, url_for, flash, session
from app import app, users, supervisor_allocation, submitted_projects, project_reviews
from app import generate_supervisor_notification, generate_project_approval_notification

@app.route('/')
def index():
    return "Welcome to the Student Supervisor Allocation System!"

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Login logic (already implemented)
    pass

@app.route('/student_dashboard')
def student_dashboard():
    # Student dashboard logic (already implemented)
    pass

@app.route('/lecturer_dashboard')
def lecturer_dashboard():
    # Lecturer dashboard logic (already implemented)
    pass

@app.route('/admin_dashboard')
def admin_dashboard():
    # Admin dashboard logic (already implemented)
    pass

@app.route('/notifications')
def notifications():
    # Get notifications for the logged-in user
    user_email = session.get('email')  # Assuming the user's email is stored in the session
    user_notifications = users.get(user_email, {}).get('notifications', [])
    return render_template('notifications.html', notifications=user_notifications)

@app.route('/allocate_supervisor', methods=['POST'])
def allocate_supervisor():
    # Supervisor allocation logic (already implemented)
    pass

@app.route('/approve_project', methods=['POST'])
def approve_project():
    # Project approval logic (already implemented)
    pass

@app.route('/reject_project', methods=['POST'])
def reject_project():
    # Project rejection logic (already implemented)
    pass

@app.route('/search_project', methods=['GET'])
def search_project():
    # Search logic (already implemented)
    pass

@app.route('/project_details/<title>')
def project_details(title):
    # Get project details (you should replace this with your actual logic)
    project_details = get_project_details(title)
    
    # Get existing reviews and ratings for the project
    project_reviews_data = project_reviews.get(title, {'reviews': [], 'ratings': []})
    
    return render_template('project_details.html', project_details=project_details, project_reviews=project_reviews_data)

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
