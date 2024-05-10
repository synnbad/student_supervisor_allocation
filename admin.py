# admin.py

from flask import render_template, request, redirect, url_for, flash, session
from app import app, supervisor_allocation, submitted_projects
from flask import Blueprint

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/')
def index():
    if 'email' not in session or session['role'] != 'admin':
        return redirect(url_for('auth.login'))

    allocated_students = supervisor_allocation
    pending_projects = submitted_projects

    return render_template('admin_dashboard.html', students=allocated_students, projects=pending_projects)
    return render_template('admin_dashboard.html', students=allocated_students, projects=all_projects)

# Add other admin-related routes such as user management functionalities
