from flask import Blueprint

def create_notifications_blueprint():
    notifications_bp = Blueprint('notifications', __name__, template_folder='templates')
    @notifications_bp.route('/notifications')
    def display_notifications():
        user_notifications = session.get('notifications', [])
        return render_template('notifications.html', notifications=user_notifications)

    return notifications_bp
