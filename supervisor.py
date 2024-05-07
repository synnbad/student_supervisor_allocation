# supervisor.py

from flask import render_template, request, redirect, url_for, flash, session
from app import app, supervisor_allocation

@app.route('/allocate_supervisor', methods=['POST'])
def allocate_supervisor():
    if 'email' not in session or session['role'] != 'admin':
        return redirect(url_for('login'))

    email = request.form['email']
    supervisor_name = request.form['supervisor_name']

    supervisor_allocation[email] = supervisor_name

    return redirect(url_for('admin_dashboard'))


# Add other supervisor-related routes if needed
