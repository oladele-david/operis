from app.extensions import db
from sqlalchemy.dialects.postgresql import UUID
import uuid


class UserBusinessAssociation(db.Model):
    """
    Represents the association between users and businesses, including the user's role.
    """
    __tablename__ = 'user_business_association'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=False)
    business_id = db.Column(UUID(as_uuid=True), db.ForeignKey('businesses.id'), nullable=False)
    role = db.Column(db.String(50), nullable=False, default='staff')  # e.g., 'staff', 'owner'
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    # Relationships
    user = db.relationship("User", back_populates="business_associations")
    business = db.relationship("Business", back_populates="user_associations")

    def __repr__(self):
        return f"<UserBusinessAssociation user_id={self.user_id} business_id={self.business_id} role={self.role}>"
