from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, jsonify
from flask_login import login_user, login_required, logout_user
from psycopg2.errors import UniqueViolation
from sqlalchemy.exc import IntegrityError

from app.crud.auth import create_business_and_user, login_user_to_business
from app.extensions import db
from app.models import User, Business

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


@auth_bp.route('/search-business', methods=['POST'])
def search_business():
    """Search for businesses by name."""
    search_term = request.form.get('q', '').strip()
    if not search_term:
        return jsonify([])

    businesses = Business.query.filter(Business.name.ilike(f"%{search_term}%")).all()
    suggestions = [{'value': business.name, 'id': str(business.id)} for business in businesses]
    return jsonify(suggestions)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Login route where users select a business and authenticate."""
    if request.method == 'POST':
        business_id = request.form.get('businessSearch')
        email = request.form.get('email')
        password = request.form.get('password')

        try:
            # Process login via CRUD function
            user, business, role = login_user_to_business(email, password, business_id)

            success_message = f"Welcome {user.first_name}! You are logged into {business.name} as {role}."
            if request.headers.get('HX-Request'):
                return render_template('auth/login_success.html', mmessage=success_message, business_name=business.name,
                    redirect_url=url_for('dashboard_route.dashboard'))

            flash(success_message, "success")
            return redirect(url_for('dashboard_route.dashboard'))

        except ValueError as e:
            error_message = str(e)
            if request.headers.get('HX-Request'):
                return render_template('auth/login_error.html', error=error_message)
            flash(error_message, "error")
            return render_template('auth/login.html')

    # GET request: Render the login page
    return render_template('auth/login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('auth_route.login'))