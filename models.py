from database import Base
from sqlalchemy import Column, Integer, String, Boolean, Text,ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy_utils.types import ChoiceType



class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(25), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    password = Column(Text, nullable=True)
    hashed_password = Column(String(128))
    is_staff = Column(Boolean, default=True)
    is_active = Column(Boolean, default=False)
    orders = relationship("Choice", back_populates="user")



    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}', is_staff={self.is_staff}, is_active={self.is_active})>"
    


class Choice(Base):
    

    ORDER_STATUS_CHOICES = (
        ("PENDING", "Pending"),
        ("IN_TRANSIT", "In Transit"),
        ("DELIVERED", "Completed"),
        ("CANCELLED", "Cancelled"),
    
)



    PIZZA_SIZES= (
                ("SMALL", "Small"),
                ("MEDIUM", "Medium"),
                ("LARGE", "Large"),
                ("EXTRA_LARGE", "Extra Large"),
    )
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    quantity = Column(Integer, nullable=False)
    name = Column(String(100), unique=True, index=True)
    description = Column(Text, nullable=True)
    status = Column(ChoiceType(choices=ORDER_STATUS_CHOICES), default="PENDING", nullable=False)
    pizza_size = Column(ChoiceType(choices=PIZZA_SIZES), default="MEDIUM", nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    user=relationship("User", back_populates="orders")

    def __repr__(self):
        return f"<Order(id={self.id}, name='{self.name}', description='{self.description}', status='{self.status}', pizza_size='{self.pizza_size}', user_id={self.user_id})>"
    
