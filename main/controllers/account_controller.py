from sqlalchemy.orm import Session
from ..models.account import Account
from ..models.login import Login
from ..models.roles import RoleEnum

class AccountController:
    def __init__(self, db: Session):
        self.db = db

    # It is only possible to create a User account via code, not an admin
    # Equivalent to Register() method from the design
    def create_user_account(self, firstname: str, lastname: str, dateOfBirth: str, email: str, username: str, password: str) -> Account:
        # Enforce password policy
        if not Login.validate_password(username, password):
            raise ValueError("Password does not meet the password policy requirements.")
        
        # Create a new user account
        new_account = Account(
            firstname=firstname,
            lastname=lastname,
            dateOfBirth=dateOfBirth,
            email=email,
            role=RoleEnum.USER
        )

        # Create a login for the user
        salt = Login.generate_salt()
        hashed_password = Login.hash_password(password, salt)
        new_login = Login(
            username=username, 
            password=hashed_password,
            salt=salt,
            account=new_account
        )

        # Add the new user and login to the database
        self.db.add(new_account)
        self.db.add(new_login)
        self.db.commit()

        return new_account

    def verify_login(self, username: str, password: str) -> bool:
        login = self.db.query(Login).filter(Login.username == username).first()
        if not login:
            return False
        return Login.verify_password(password, login.password)

    def get_user_by_username(self, username: str) -> Account:
        """Retrieve an account by username."""
        login = self.db.query(Login).filter(Login.username == username).first()
        if login:
            return login.account
        else:
            return None

    def get_user_by_email(self, email: str) -> Account:
        """Retrieve an account by email."""
        return self.db.query(Account).filter(Account.email == email).first()
