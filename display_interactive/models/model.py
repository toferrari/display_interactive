from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

Base = declarative_base()


class Purchases(Base):
    __tablename__ = 'purchases'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    customer_id = Column(Integer, ForeignKey('customers.customer_id'), nullable=False)
    product_id = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False)
    currency = Column(String, nullable=False)
    date = Column(String, nullable=False)
    submitted = Column(Boolean, default=False, nullable=False)

    customer = relationship("Customers", back_populates="purchases")

    def to_dict(self):
        return {
            "id": str(self.id),
            "customer_id": self.customer_id,
            "product_id": self.product_id,
            "price": self.price,
            "quantity": self.quantity,
            "currency": self.currency,
            "date": self.date,
        }



class Customers(Base):
    __tablename__ = 'customers'

    customer_id = Column(Integer, nullable=False, primary_key=True)
    title = Column(Integer, nullable=True)
    last_name = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    postal_code = Column(String, nullable=True)
    email = Column(String, nullable=True)
    submitted = Column(Boolean, default=False, nullable=False)

    purchases = relationship("Purchases", back_populates="customer")

    def to_dict(self):
        return {
            "customer_id": self.customer_id,
            "title": self.title,
            "last_name": self.last_name,
            "first_name": self.first_name,
            "postal_code": self.postal_code,
            "email": self.email,
            "purchases": [purchase.to_dict() for purchase in self.purchases]
        }