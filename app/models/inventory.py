import uuid
from sqlalchemy.dialects.postgresql import UUID
from app.extensions import db


class Inventory(db.Model):
    """
    Represents the inventory for products in a business.
    """
    __tablename__ = 'inventory'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    product_id = db.Column(UUID(as_uuid=True), db.ForeignKey('products.id', ondelete="CASCADE"), nullable=False, index=True)
    business_id = db.Column(UUID(as_uuid=True), db.ForeignKey('businesses.id', ondelete="CASCADE"), nullable=False, index=True)
    quantity_available = db.Column(db.Float, nullable=False, default=0)
    last_restocked_at = db.Column(db.DateTime, nullable=True)

    # Relationships
    product = db.relationship('Product', back_populates="inventory")
    business = db.relationship("Business", back_populates="inventory")

    def __repr__(self):
        return f"<Inventory {self.id} (Quantity: {self.quantity_available})>"
