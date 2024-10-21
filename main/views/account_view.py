import sys
from getpass import getpass
from datetime import datetime
from sqlalchemy.orm import Session
from ..controllers.account_controller import AccountController
from .musicartefact_view import MusicArtefactCLIView
from ..models.account import Account

class AuthenticationView:
    def __init__(self, db_session: Session):
        self.db_session = db_session
        self.account_controller = AccountController(db_session)
        self.current_account = None

    def display_menu(self):
        print("Welcome to the Music Artefact Management CLI")
        print("1. Register")
        print("2. Log in")
        print("3. Exit")

    def openMusicArtefactView(self):
        musicArtefactCLIView = MusicArtefactCLIView(self.db_session, self.current_account)
        musicArtefactCLIView.run()

    def register(self):
        print("Please fill out the following information to register")
        firstname = input("First Name: ").strip()
        lastname = input("Last Name: ").strip()
        dateOfBirth_str = input("Date of Birth (YYYY-MM-DD): ").strip()
        dateOfBirth = datetime.strptime(dateOfBirth_str , '%Y-%m-%d')
        print(f"{dateOfBirth}")
        email = input("Email: ").strip()
        username = input("Username: ").strip()
        password = getpass("Password: ").strip()

        try:

            account = self.account_controller.create_user_account(firstname, lastname, dateOfBirth, email, username, password)
            print(f"Registration successful. Welcome, {account.firstname} {account.lastname}!")
            self.current_account = account
            self.openMusicArtefactView()
        except Exception as e:
            print(f"Registration failed: {e}")

    def login(self):
        while True:
            print("Please log in to continue")
            username = input("Username: ").strip()
            password = getpass("Password: ").strip()

            if self.account_controller.verify_login(username, password):
                account = self.account_controller.get_user_by_username(username)
                print(f"Welcome, {account.firstname} {account.lastname}")
                self.current_account = account
                self.openMusicArtefactView()
                break
            else:
                print("Invalid username or password. Please try again.")

    def run(self):
        while True:
            self.display_menu()
            choice = input("Please select an option: ").strip()
            if choice == '1':
                self.register()
            elif choice == '2':
                self.login()
            elif choice == '3':
                print("Goodbye!")
                sys.exit(0)
            else:
                print("Invalid choice. Please try again.")
    
