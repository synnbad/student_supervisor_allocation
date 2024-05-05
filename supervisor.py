# supervisor.py

from flask import render_template, request, redirect, url_for, flash, session
from app import app, supervisor_allocation

@app.route('/allocate_supervisor', methods=['POST'])
def allocate_supervisor():
    if 'email' not in session or session['role'] != 'admin':
        flash('You are not authorized to perform this action.', 'error')
        return redirect(url_for('login'))

    # Handle supervisor allocation logic here
    # For example, retrieve student email and supervisor name from the form and update supervisor_allocation
    return redirect(url_for('admin_dashboard'))

# Add other supervisor-related routes if needed
