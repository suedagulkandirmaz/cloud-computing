from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from .database import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)

    customer_name = Column(String(100), nullable=False)

    product_id = Column(Integer, nullable=False)

    quantity = Column(Integer, nullable=False)

    total_price = Column(Float, nullable=False)

    status = Column(String(30), nullable=False, default="QUEUED")

    created_at = Column(DateTime, default=datetime.utcnow)

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )