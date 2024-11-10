from sqlalchemy.dialects.postgresql import UUID
import uuid
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db


class User(UserMixin, db.Model):
    """
    Represents a system user, either a business owner or a staff member.
    """
    __tablename__ = 'users'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    phone_number = db.Column(db.String(20), unique=True, nullable=True)
    password_hash = db.Column(db.String(255), nullable=False)
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
        return f"<User {self.id}, {self.first_name} {self.last_name}, {self.email}, {self.phone_number}>"

    def set_password(self, password):
        """Hashes and sets the user's password."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Validates a password against the stored hash."""
        return check_password_hash(self.password_hash, password)

    @property
    def current_business(self):
        # Import UserBusinessAssociation here to avoid circular imports
        from app.models.user_business_association import UserBusinessAssociation
        association = UserBusinessAssociation.query.filter_by(user_id=self.id, role='owner').first()
        return association.business if association else None

    @property
    def business_role(self):
        # Import UserBusinessAssociation here to avoid circular imports
        from app.models.user_business_association import UserBusinessAssociation
        association = UserBusinessAssociation.query.filter_by(user_id=self.id).first()
        return association.role if association else None
