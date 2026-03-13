import uuid
from sqlalchemy import Column, String, Numeric
from shared.db import Base

class Subscription(Base):
    __tablename__ = "subscriptions"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    platform_id = Column(String, nullable=False)
    user_id = Column(String, nullable=False)
    status = Column(String, nullable=False)
    price_amount = Column(Numeric, nullable=False)
    price_denom = Column(String, nullable=False)

class Payment(Base):
    __tablename__ = "payments"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    platform_id = Column(String, nullable=False)
    user_id = Column(String, nullable=False)
    amount = Column(Numeric, nullable=False)
    denom = Column(String, nullable=False)
    tx_hash = Column(String, nullable=True)
