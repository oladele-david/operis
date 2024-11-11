from flask import session

from app.models import User, Business, UserBusinessAssociation
from app.extensions import db, login_manager
from flask_login import login_user
from uuid import uuid4
from werkzeug.security import generate_password_hash

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(str(user_id))

def create_business_and_user(business_name, first_name, last_name, phone_number, email, password):
    try:
        # Create Business
        business_id = uuid4()  # Create unique business ID
        business = Business(
            id=business_id,
            name=business_name
        )
        db.session.add(business)

        # Create User
        user = User(
            id=uuid4(),
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            email=email,
            password_hash=generate_password_hash(password),
        )
        db.session.add(user)

        # Create User-Business Association (Owner role)
        user_business_association = UserBusinessAssociation(
            user_id=user.id,
            business_id=business.id,
            role='owner'  # User role as owner
        )
        db.session.add(user_business_association)

        # Commit the transaction to save everything to the database
        db.session.commit()

        # Log in the user
        login_user(user)

        return user, business

    except Exception as e:
        db.session.rollback()
        raise e

def authenticate_user(email, password):
    """
    Authenticate the user by email and password.
    Returns the user if successful, or raises an exception.
    """
    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        raise ValueError("Invalid email or password.")
    return user

def check_user_business_association(user_id, business_id):
    """
    Check if the user is associated with the specified business.
    Returns the association if successful, or raises an exception.
    """
    association = UserBusinessAssociation.query.filter_by(user_id=user_id, business_id=business_id).first()
    if not association:
        raise ValueError("You do not have access to this business.")
    return association

def login_user_to_business(email, password, business_id):
    """
    Handle the complete login process:
    1. Authenticate the user.
    2. Verify user's association with the business.
    3. Log in the user and set session data.
    """
    # Authenticate the user
    user = authenticate_user(email, password)

    # Find the business by name
    user_business = Business.query.filter_by(id=business_id).first()
    if not user_business:
        raise ValueError("Business not found. Please select a valid business.")

    # Check user-business association
    association = check_user_business_association(user.id, user_business.id)

    # Log the user in and set session data
    login_user(user)
    session['user_id'] = str(user.id)
    session['business_id'] = str(user_business.id)
    session['business_name'] = user_business.name
    session['role'] = association.role

    return user, user_business, association.role