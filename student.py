# student.py

from flask import Blueprint

student_bp = Blueprint('student', __name__)

@student_bp.route('/dashboard')
def student_dashboard():
    """Display the student dashboard."""
    return render_template('student_dashboard.html')

@student_bp.route('/projects')
def student_projects():
    """Display projects submitted by the student"""
    pass
    pass

@student_bp.route('/supervisor')
def supervisor_info():
    """Display assigned supervisor information"""
    pass
