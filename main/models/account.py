from sqlalchemy import Column, String, Date, Integer, Enum, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base
from .roles import RoleEnum

class Account(Base):
    __tablename__ = 'accounts'
    id = Column(Integer, primary_key=True, index=True)
    firstname = Column(String(50), nullable=False)
    lastname = Column(String(50), nullable=False)
    dateOfBirth = Column(Date, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    role = Column(Enum(RoleEnum), nullable=False)
    
    login = relationship("Login", back_populates="account", uselist=False)
    
    music_artefacts = relationship("MusicArtefact", back_populates="account")


    def get_username(self):
        return self.login.username if self.login else None