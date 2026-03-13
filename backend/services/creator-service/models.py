import uuid
from sqlalchemy import Column, String, JSON
from shared.db import Base

class Creator(Base):
    __tablename__ = "creators"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    handle = Column(String, nullable=False, unique=True)
    wallet_address = Column(String, nullable=False)

class Platform(Base):
    __tablename__ = "platforms"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    creator_id = Column(String, nullable=False)
    name = Column(String, nullable=False)
    monetization_type = Column(String, nullable=False)
    pricing_model = Column(JSON, nullable=False)
