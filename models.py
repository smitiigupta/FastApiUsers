from sqlalchemy import Column, Integer, String
from database import Base

# Define User class inheriting from Base
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(256))
    age = Column(Integer)
    gender = Column(String(10))
    address = Column(String(500))