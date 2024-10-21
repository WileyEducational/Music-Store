from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base
import re
import bcrypt

class Login(Base):
    __tablename__ = 'logins'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(60), nullable=False)
    salt = Column(String(29), nullable=False)

    account_id = Column(Integer, ForeignKey('accounts.id'))

    account = relationship("Account", back_populates="login", uselist=False)
    

    @staticmethod
    def hash_password(password: str, salt: str) -> str:
        return bcrypt.hashpw(password.encode('utf-8'), salt.encode('utf-8')).decode('utf-8')

    @staticmethod
    def verify_password(password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

    @staticmethod
    def generate_salt() -> str:
        return bcrypt.gensalt().decode('utf-8')
    
    
    #Password policy based on NIST 800-63B, can be altered where needed
    @staticmethod
    def validate_password(username: str, password: str) -> bool:
        # Password should be at least 8 characters long
        if len(password) < 8:
            return False
        
        # Password should not exceed 64 characters
        if len(password) > 64:
            return False
        
        # Password should not contain username
        if username.lower() in password.lower():
            return False
        
        # Password should not be a common dictionary word or variation
        common_words = ['password', '123456', 'qwerty', 'welcome', 'login', 'letmein']
        for word in common_words:
            if word.lower() in password.lower():
                return False
        
        # Password should contain at least one uppercase letter
        if not re.search(r'[A-Z]', password):
            return False
        
        # Password should contain at least one lowercase letter
        if not re.search(r'[a-z]', password):
            return False
        
        # Password should contain at least one digit
        if not re.search(r'\d', password):
            return False
        
        # Password should contain at least one special character
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            return False
        
        return True
