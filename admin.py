# admin.py

from flask import render_template, request, redirect, url_for, flash, session
from app import app, supervisor_allocation, submitted_projects

@app.route('/admin_dashboard')
def admin_dashboard():
    if 'email' not in session or session['role'] != 'admin':
        flash('You need to be logged in as an admin to access this page.', 'error')
        return redirect(url_for('login'))

    # Retrieve data needed for the admin dashboard
    allocated_students = supervisor_allocation
    all_projects = submitted_projects

    return render_template('admin_dashboard.html', students=allocated_students, projects=all_projects)

# Add other admin-related routes such as user management functionalities
