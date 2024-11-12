import uuid
from sqlalchemy.dialects.postgresql import UUID
from app.extensions import db


class Finance(db.Model):
    """
    Represents financial records such as expenses and revenues for a business.
    """
    __tablename__ = 'finance'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    business_id = db.Column(UUID(as_uuid=True), db.ForeignKey('businesses.id', ondelete="CASCADE"), nullable=False, index=True)
    description = db.Column(db.String(200), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    type = db.Column(db.String(50), nullable=False)  # 'income' or 'expense'
    date = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())

    # Relationship with business
    business = db.relationship("Business", back_populates="finances")

    def __repr__(self):
        return f"<Finance {self.type}: {self.description} (${self.amount})>"
