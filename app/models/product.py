import uuid
from sqlalchemy.dialects.postgresql import UUID
from app.extensions import db


class Product(db.Model):
    """
    Represents a product sold by a business.
    """
    __tablename__ = 'products'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(150), nullable=False, index=True)
    type = db.Column(db.String(50), nullable=False)  # Examples: "fuel", "oil"
    price_per_unit = db.Column(db.Float, nullable=False)
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
    business_id = db.Column(UUID(as_uuid=True), db.ForeignKey('businesses.id', ondelete="CASCADE"), nullable=False, index=True)

    # Relationships
    inventory = db.relationship('Inventory', back_populates="product", lazy="select")

    def __repr__(self):
        return f"<Product {self.id} (Name: {self.name})>"
