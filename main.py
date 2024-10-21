from datetime import datetime
from sqlalchemy.orm import Session
from main.database import get_db
from main.controllers.account_controller import AccountController

from main.views.account_view import AuthenticationView

from sqlalchemy import create_engine
from main.database import Base, DATABASE_URL

def main():
    # Get a database session
    db: Session = next(get_db())

    # Start the authentication view
    authentication_view = AuthenticationView(db)
    authentication_view.run()

if __name__ == "__main__":
    main()