from sqlalchemy import Boolean, Column, Integer, String
from database import Base


Class Client(Base):
    __tablename__ = 'clients'
    id = Column(Integer)

