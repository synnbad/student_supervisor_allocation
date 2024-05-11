# supervisor.py

from flask import Blueprint, redirect, request, url_for, session
from app import supervisor_allocation

supervisor_bp = Blueprint('supervisor', __name__)

@supervisor_bp.route('/allocate_supervisor', methods=['POST'])
def allocate_supervisor():
    """Allocate a supervisor to a student."""
    if 'email' not in session or session.get('role') != 'admin':
        # Redirect if user is not logged in as admin
        return redirect(url_for('auth.login'))

    # Get form data
    email = request.form['email']
    supervisor_name = request.form['supervisor_name']

    # Assign supervisor to student
    supervisor_allocation[email] = supervisor_name

    # Redirect to admin dashboard
    return redirect(url_for('admin.dashboard'))

# Add other supervisor-related routes if needed
