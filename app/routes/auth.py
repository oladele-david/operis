from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_user, login_required, logout_user
from psycopg2.errors import UniqueViolation
from sqlalchemy.exc import IntegrityError

from app.crud.auth import create_business_and_user
from app.extensions import db
from app.models import User

auth_bp = Blueprint('auth_route', __name__)


@auth_bp.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        business_name = request.form.get('businessName')
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        phone_number = request.form.get('phoneNumber')
        email = request.form.get('email')
        password = request.form.get('password')

        try:
            # Create business and user
            user, business = create_business_and_user(
                business_name, first_name, last_name, phone_number, email, password
            )

            business_name = user.current_business.name

            # If the request is from HTMX
            if request.headers.get('HX-Request'):
                success_message = "Signup successful! Redirecting to your dashboard..."
                return render_template(
                    'auth/signup_success.html',
                    message=success_message, business_name=business_name,
                    redirect_url=url_for('dashboard_route.dashboard')
                )

            # For non-HTMX requests
            flash("Signup successful! You are now logged in.", 'success')
            return redirect(url_for('dashboard_route.dashboard'))

        except IntegrityError as e:
            db.session.rollback()  # Rollback transaction
            if isinstance(e.orig, UniqueViolation):
                current_app.logger.error(f"IntegrityError: {e}")
                if request.headers.get('HX-Request'):
                    return render_template(
                        'auth/signup_error.html',
                        error="A business or account with this information already exists."
                    )
                flash("A business or account with this information already exists.", 'error')
            else:
                current_app.logger.error(f"Unknown IntegrityError: {e}")
                if request.headers.get('HX-Request'):
                    return render_template(
                        'auth/signup_error.html',
                        error="An unknown error occurred. Please try again."
                    )
                flash("An unknown error occurred. Please try again.", 'error')

        except Exception as e:
            current_app.logger.error(f"Unexpected Error: {e}")
            if request.headers.get('HX-Request'):
                return render_template('auth/signup_error.html',
                                       error="Unexpected error occurred. Please try again.")
            flash("Unexpected error occurred. Please try again.", 'error')

    return render_template('auth/signup.html')  # Render signup form for GET requests


@auth_bp.route('/check-email', methods=['POST'])
def check_email():
    email = request.form.get('email')
    if "@" not in email:
        return "Invalid email format"
    # Here you could also check if the email is already taken
    return "Email is available"


@auth_bp.route('/validate-password', methods=['POST'])
def validate_password():
    password = request.form.get('password')
    if len(password) < 8:
        return "Password must be at least 8 characters", 200
    return "Password strength: Good", 200


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            login_user(user)
            flash("Login successful!", 'success')
            return redirect(url_for('dashboard_route.dashboard'))
    return render_template('auth/login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('auth_route.login'))