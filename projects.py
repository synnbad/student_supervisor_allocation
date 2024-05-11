from flask import Blueprint

def create_projects_blueprint():
    projects_bp = Blueprint('projects', __name__)
    # This route is called when a student submits a project
    # The POST request contains the project details
    @projects_bp.route('/submit_project', methods=['POST'])
    def submit_project():
        # Check if the student is logged in
        if 'email' not in session:
            # If not, redirect the student to the login page
            flash('You need to be logged in to access this page.', 'error')
            return redirect(url_for('auth.login'))

        # Retrieve project details from the form
        project_title = request.form['project_title']
        project_description = request.form['project_description']
        project_type = request.form['project_type']
        project_supervisor = request.form['project_supervisor']

        # Add the new project to the list of submitted projects
        submitted_projects[session['email']] = {
            'title': project_title,
            'description': project_description,
            'type': project_type,
            'supervisor': project_supervisor,
            'status': 'pending'
        }

        # Redirect the student to their dashboard
        return redirect(url_for('student.dashboard'))

    # Add other project-related routes such as project details, approval, and rejection

    return projects_bp
