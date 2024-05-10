from app import users

# Define utility functions here

def generate_supervisor_notification(student_email, supervisor_name):
    notification_message = f"Your supervisor has been updated. Your new supervisor is {supervisor_name}."
    users[student_email]['notifications'].append(notification_message)

def generate_project_approval_notification(student_email, project_title, approval_status):
    if approval_status == 'approved':
        notification_message = f"Congratulations! Your project '{project_title}' has been approved."
    else:
        notification_message = f"We regret to inform you that your project '{project_title}' has been rejected."
    users[student_email]['notifications'].append(notification_message)
