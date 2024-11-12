import uuid
from sqlalchemy.dialects.postgresql import UUID
from app.extensions import db


class RestockHistory(db.Model):
    """
    Tracks restocking events for products.
    """
    __tablename__ = 'restock_history'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    product_id = db.Column(UUID(as_uuid=True), db.ForeignKey('products.id', ondelete="CASCADE"), nullable=False, index=True)
    business_id = db.Column(UUID(as_uuid=True), db.ForeignKey('businesses.id', ondelete="CASCADE"), nullable=False, index=True)
    restocked_quantity = db.Column(db.Float, nullable=False)
    restocked_by = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=False)
    restocked_at = db.Column(db.DateTime, default=db.func.now())

    def __repr__(self):
        return f"<RestockHistory {self.id} (Product: {self.product_id})>"
