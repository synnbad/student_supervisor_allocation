from flask import Flask, render_template, request, redirect, url_for, flash, session
from app import app, users, supervisor_allocation, submitted_projects, project_reviews
from app import generate_supervisor_notification, generate_project_approval_notification
from werkzeug.exceptions import abort

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Welcome page
@app.route("/")
def index():
    return "Welcome to the Student Supervisor Allocation System!"


# User login
@app.route("/login", methods=["GET", "POST"])
def login():
    # Login logic
    # ...

    # Student dashboard
    @app.route("/student_dashboard")
    def student_dashboard():
        # Student dashboard logic
        # ...

        # Lecturer dashboard
        @app.route("/lecturer_dashboard")
        def lecturer_dashboard():
            # Lecturer dashboard logic
            # ...

            # Admin dashboard
            @app.route("/admin_dashboard")
            def admin_dashboard():
                # Admin dashboard logic
                # ...

                # Notifications
                @app.route("/notifications")
                def notifications():
                    # Notifications logic
                    # ...

                    # Allocate supervisor
                    @app.route("/allocate_supervisor", methods=["POST"])
                    def allocate_supervisor():
                        # Allocate supervisor logic
                        # ...

                        # Approve project
                        @app.route("/approve_project", methods=["POST"])
                        def approve_project():
                            # Approve project logic
                            # ...

                            # Reject project
                            @app.route("/reject_project", methods=["POST"])
                            def reject_project():
                                # Reject project logic
                                # ...

                                # Search project
                                @app.route("/search_project", methods=["GET"])
                                def search_project():
                                    # Search project logic
                                    # ...

                                    # Project details
                                    @app.route("/project_details/<title>")
                                    def project_details(title):
                                        # Project details logic
                                        # ...

                                        # Profile edit
                                        @app.route(
                                            "/profile_edit", methods=["GET", "POST"]
                                        )
                                        def profile_edit():
                                            # Profile edit logic
                                            # ...

                                            # Reset password
                                            @app.route(
                                                "/reset_password", methods=["POST"]
                                            )
                                            def reset_password():
                                                # Reset password logic
                                                # ...

                                                # Delete account
                                                @app.route(
                                                    "/delete_account", methods=["POST"]
                                                )
                                                def delete_account():
                                                    # Delete account logic
                                                    # ...

                                                    # Submit review
                                                    @app.route(
                                                        "/submit_review",
                                                        methods=["POST"],
                                                    )
                                                    def submit_review():
                                                        # Submit review logic
                                                        # ...

                                                        if __name__ == "__main__":
                                                            app.run(debug=True)
