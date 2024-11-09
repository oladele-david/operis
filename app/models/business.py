import uuid
from app.extensions import db


class Business(db.Model):
    """
    Represents a business that can have multiple staff and owners.
    """
    __tablename__ = 'businesses'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    # Association with users
    user_associations = db.relationship(
        'UserBusinessAssociation', back_populates='business', cascade="all, delete-orphan"
    )

    # Derived relationship (view-only)
    users = db.relationship(
        'User', secondary='user_business_association', viewonly=True
    )

    inventory_items = db.relationship(
        "Inventory", back_populates="business", cascade="all, delete-orphan"
    )

    financial_records = db.relationship(
        "Finance", back_populates="business", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Business {self.name}>"
