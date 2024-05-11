# users.py

from flask import Blueprint, render_template, request, redirect, url_for, flash, session

users_bp = Blueprint('users', __name__)

@users_bp.route('/profile_edit', methods=['GET', 'POST'])
def profile_edit():
    """Edit user profile."""
    if 'email' not in session:
        flash('You need to be logged in to access this page.', 'error')
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        email = session['email']
        name = request.form['name']
        users[email]['name'] = name
        flash('Profile updated successfully', 'success')
        return redirect(url_for('users.profile_edit'))
    else:
        user_email = session['email']
        return render_template('profile_edit.html', user=users[user_email])
