import uuid
from sqlalchemy.dialects.postgresql import UUID
from app.extensions import db


class Business(db.Model):
    """
    Represents a business that can have multiple staff and owners.
    """

    __tablename__ = 'businesses'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(100), nullable=False, unique=True, index=True)
    description = db.Column(db.Text, nullable=True)
    location = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)
    updated_at = db.Column(
        db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp()
    )

    # Many-to-Many Association with Users
    user_associations = db.relationship(
        'UserBusinessAssociation', back_populates='business', cascade="all, delete-orphan"
    )

    # Read-only Derived Relationship for Users
    users = db.relationship(
        'User', secondary='user_business_association', viewonly=True
    )

    # One-to-Many Relationships
    inventory = db.relationship(
        "Inventory", back_populates="business", cascade="all, delete-orphan", lazy="select"
    )
    finances = db.relationship(
        "Finance", back_populates="business", cascade="all, delete-orphan", lazy="select"
    )
    products = db.relationship('Product', backref='business', lazy="select")
    sales = db.relationship('Sale', backref='business', lazy="select")
    restock_history = db.relationship('RestockHistory', backref='business', lazy="select")

    def __repr__(self):
        """
        Returns a string representation of the Business instance.
        """
        return f"<Business {self.id}, {self.name}, {self.description}>"
