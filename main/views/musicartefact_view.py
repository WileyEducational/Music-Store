import sys
from datetime import datetime
from sqlalchemy.orm import Session
from ..controllers.musicartefact_controller import MusicArtefactController
from ..models.account import Account
from ..models.artefacttypes import MusicArtefactType

class MusicArtefactCLIView:
    def __init__(self, db_session: Session, current_account: Account):
        self.db_session = db_session
        self.musicartefact_controller = MusicArtefactController(db_session)
        self.current_account = current_account

    def display_menu(self):
        print("Music Artefact Management Menu")
        print("1. Create Music Artefact")
        print("2. View Music Artefact")
        print("3. View All Music Artefacts")
        print("4. Update Music Artefact")
        print("5. Delete Music Artefact")
        print("6. Exit")

    def run(self):
        while True:
            self.display_menu()
            choice = input("Please select an option: ").strip()
            if choice == '1':
                self.create_artefact()
            elif choice == '2':
                self.view_artefact()
            elif choice == '3':
                self.view_all_artefacts()
            elif choice == '4':
                self.update_artefact()
            elif choice == '5':
                self.delete_artefact()
            elif choice == '6':
                print("Goodbye!")
                sys.exit(0)
            else:
                print("Invalid choice. Please try again.")

    def create_artefact(self):
        artefact_type_input = input("Enter artefact type (1: recording, 2: lyrics, 3: score): ").strip()
        pathtofile = input("Enter the path to the file: ").strip()
        creationdate = datetime.now()
        lastmodifieddate = datetime.now()
        isdeleted = False

        try:
            artefact_type = MusicArtefactType(int(artefact_type_input))
        except ValueError:
            print("Invalid artefact type. Please enter 1, 2, or 3.")
            return

        try:
            artefact, uploaded_file_path = self.musicartefact_controller.create_music_artefact(
                self.current_account,
                pathtofile,
                artefact_type = artefact_type,
                creationdate=creationdate,
                lastmodifieddate=lastmodifieddate,
                isdeleted=isdeleted
            )
            print(f"Created {artefact_type} artefact: {artefact}")
            print(f"File uploaded to: {uploaded_file_path}")
        except Exception as e:
            print(f"Failed to create artefact: {e}")

    def view_artefact(self):
        artefact_id = int(input("Enter the artefact ID: ").strip())
        artefact = self.musicartefact_controller.view_music_artefact(artefact_id)
        if artefact:
            artefact.print_details()
        else:
            print("Artefact not found.")

    def view_all_artefacts(self):
        artefacts = self.musicartefact_controller.view_all_music_artefacts()
        for artefact in artefacts:
            artefact.print_details()

    def update_artefact(self):
        artefact_id = int(input("Enter the artefact ID: ").strip())
        new_pathtofile = input("Enter the new path to the file (leave blank to keep current): ").strip()

        new_data = {}
        if new_pathtofile:
            new_data['pathtofile'] = new_pathtofile

        artefact = self.musicartefact_controller.update_music_artefact(artefact_id, self.current_account, new_data)
        if artefact:
            print(f"Updated artefact: {artefact}")
        else:
            print("Failed to update artefact or unauthorized action.")

    def delete_artefact(self):
        artefact_id = int(input("Enter the artefact ID: ").strip())
        soft_delete = input("Soft delete? (yes/no): ").strip().lower() == 'yes'

        if soft_delete:
            success = self.musicartefact_controller.soft_delete_music_artefact(artefact_id, self.current_account)
        else:
            success = self.musicartefact_controller.hard_delete_music_artefact(artefact_id, self.current_account)