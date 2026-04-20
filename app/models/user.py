from sqlalchemy import Column, String, DateTime, Integer
from core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    First_Name = Column(String)
    Last_Name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    Phone_Number = Column(String)

    reset_token = Column(String, nullable=True)
    reset_token_expiry = Column(DateTime, nullable=True)