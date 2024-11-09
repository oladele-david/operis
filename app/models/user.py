import uuid
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db

class User(UserMixin, db.Model):
    """
    Represents a system user, either a business owner or a staff member.
    """
    __tablename__ = 'users'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    phone_number = db.Column(db.String(20), unique=True, nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    # Association with businesses
    business_associations = db.relationship(
        'UserBusinessAssociation', back_populates='user', cascade="all, delete-orphan"
    )

    # Derived relationship (view-only)
    businesses = db.relationship(
        'Business', secondary='user_business_association', viewonly=True
    )

    def __repr__(self):
        return f"<User {self.name}, {self.email}>"

    def set_password(self, password):
        """Hashes and sets the user's password."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Validates a password against the stored hash."""
        return check_password_hash(self.password_hash, password)
