from datetime import datetime
from sqlalchemy.orm import Session
from main.database import get_db
from main.controllers.account_controller import AccountController

from sqlalchemy import create_engine
from main.database import Base, DATABASE_URL

## this is a test method to have accounts ready for demo!
def create_tables():
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(bind=engine)


def create_user_and_admin():
    # Get a database session
    db: Session = next(get_db())

    # Create an instance of the AccountController
    account_controller = AccountController(db)

    # Create a user account
    firstname = "John"
    lastname = "Doe"
    dateOfBirth = datetime(1994, 3, 10)
    email = "johndoe2@example.com"
    username = "johndoe2"
    password = "TooStronk123!"
    user = account_controller.create_user_account(firstname, lastname, dateOfBirth, email, username, password)
    print("User account created.")

    # Create an admin account
    firstname = "Admin"
    lastname = "User"
    dateOfBirth = datetime(1990, 1, 1)
    email = "admin@example.com"
    username = "adminman"
    password = "TooStronk123!"
    admin = account_controller.create_user_account(firstname, lastname, dateOfBirth, email, username, password)
    print(f"Admin {admin.get_username} account created.")

if __name__ == "__main__":
    create_tables()
    create_user_and_admin()