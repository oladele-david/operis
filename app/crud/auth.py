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
