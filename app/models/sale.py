import uuid
from sqlalchemy.dialects.postgresql import UUID
from app.extensions import db


class Sale(db.Model):
    """
    Represents a sale record in the database.
    """
    __tablename__ = 'sales'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    product_id = db.Column(UUID(as_uuid=True), db.ForeignKey('products.id', ondelete="CASCADE"), nullable=False, index=True)
    business_id = db.Column(UUID(as_uuid=True), db.ForeignKey('businesses.id', ondelete="CASCADE"), nullable=False, index=True)
    quantity = db.Column(db.Float, nullable=False, default=0)  # Default quantity for oil
    price_per_unit = db.Column(db.Float, nullable=False)
    total_cost = db.Column(db.Float, nullable=False)
    sold_by = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=False, index=True)
    date_time = db.Column(db.DateTime, default=db.func.now())

    def __repr__(self):
        return f"<Sale {self.id} (Product: {self.product_id})>"
