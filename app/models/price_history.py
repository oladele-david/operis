import uuid
from sqlalchemy.dialects.postgresql import UUID
from app.extensions import db


class PriceHistory(db.Model):
    """
    Tracks changes in product pricing.
    """
    __tablename__ = 'price_history'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    product_id = db.Column(UUID(as_uuid=True), db.ForeignKey('products.id', ondelete="CASCADE"), nullable=False, index=True)
    old_price = db.Column(db.Float, nullable=False)
    new_price = db.Column(db.Float, nullable=False)
    changed_at = db.Column(db.DateTime, default=db.func.now())
    changed_by = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=False, index=True)

    def __repr__(self):
        return f"<PriceHistory {self.id} (Product: {self.product_id})>"
