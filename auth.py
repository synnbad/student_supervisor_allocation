from flask import render_template, request, redirect, url_for, flash, session, Blueprint


def create_auth_blueprint():
    auth_bp = Blueprint('auth', __name__)
    @auth_bp.route('/login', methods=['GET', 'POST'])

    def login():
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']
            user_type = request.form['user_type']

            if email == users[user_type]['email'] and password == users[user_type]['password']:
                session['email'] = email
                session['role'] = user_type
                return redirect(url_for(f'{user_type}.dashboard'))
            else:
                flash('Invalid email or password. Please try again.', 'error')
                return redirect(url_for('auth.login'))
        else:
            return render_template('login.html')

    @auth_bp.route('/logout')
    def logout():
        session.pop('email', None)
        session.pop('role', None)
        return redirect(url_for('index'))

    # Add registration and password reset routes if needed

    return auth_bp
