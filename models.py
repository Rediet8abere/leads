from sqlalchemy import Boolean, Column, Integer, String
from database import Base


class Client(Base):
    __tablename__ = 'clients'
    id = Column(Integer, primary_key=True, index=True)
    firstname = Column(String(50))
    lastname = Column(String(50))
    email = Column(String(50), unique=True, index=True) #make email unique to avoid creating duplicate record
    resume = Column(String(50))
    state = Column(String(50), default = "PENDING")

class Attorney(Base):
    __tablename__ = 'attorney'
    id = Column(Integer, primary_key=True, index=True)
    firstname = Column(String(50))
    lastname = Column(String(50))
    email = Column(String(50))
    client_id = Column(Integer)



