from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.extensions import db

class Inventory(db.Model):
    """
    Represents the inventory of products in a business.
    """
    __tablename__ = 'inventory'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    business_id = db.Column(UUID(as_uuid=True), db.ForeignKey('businesses.id'), nullable=False)
    product_name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Float, nullable=False, default=0.0)
    price_per_unit = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    # Relationship with business
    business = db.relationship("Business", back_populates="inventory_items")

    def __repr__(self):
        return f"<Inventory {self.product_name} (Quantity: {self.quantity})>"
