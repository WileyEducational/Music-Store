from sqlite3 import IntegrityError
from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from ..models.musicartefact import MusicArtefact
from ..models.account import Account
from ..models.roles import RoleEnum
from ..models.artefacttypes import MusicArtefactType
from ..utilities.FileHandler import FileHandler

class MusicArtefactController:
    def __init__(self, db: Session):
        self.db = db

    # Equivalent to the create() method from design
    def create_music_artefact(self, performing_account: Account, pathtofile:str, **kwargs) -> MusicArtefact:
        """Create a new music artefact."""
        if performing_account.role not in [RoleEnum.ADMINISTRATOR, RoleEnum.USER]:
            raise PermissionError("Only administrators and users can create artefacts")

        if not pathtofile:
            raise ValueError("pathtofile is required")
        
        localpath = pathtofile
        pathtofile = FileHandler.uploaded_file_path(localpath)

        artefact_type = kwargs.get('artefact_type')

        if artefact_type == MusicArtefactType.RECORDING:
            if not pathtofile.lower().endswith('.mp3'):
                raise ValueError("Recording must be an .mp3 file")
        elif artefact_type == MusicArtefactType.LYRICS:
            if not pathtofile.lower().endswith('.txt'):
                raise ValueError("Lyrics must be a .txt file")
        elif artefact_type == MusicArtefactType.SCORE:
            if not pathtofile.lower().endswith('.txt'):
                raise ValueError("Score must be a .txt file")
        else:
            raise ValueError("Invalid artefact type")

        new_artefact= MusicArtefact(account=performing_account, pathtofile=pathtofile, **kwargs)

        # If database upload is successful, move file to uploads folder
        try:
            uploaded_file_path = FileHandler.copy_file_to_uploads(localpath)
            print(f"File uploaded successfully. Uploaded file path: {uploaded_file_path}")
            new_artefact.set_checksum(pathtofile)
            self.db.add(new_artefact)
            self.db.commit()
        except FileExistsError as e:
            print(f"Upload failed: {e}")

        return new_artefact, pathtofile

    def get_music_artefact(self, musicartefact_id: int) -> Optional[MusicArtefact]:
        """Retrieve a music artefact by its ID."""
        return self.db.query(MusicArtefact).filter(
            MusicArtefact.musicartefactid == musicartefact_id,
            MusicArtefact.isdeleted==False
            ).first()

    # Equivalent to the DeleteById() method from design
    def soft_delete_music_artefact(self, musicartefact_id: int, performing_account: Account) -> bool:
        """Soft delete a music artefact."""
        artefact = self.get_music_artefact(musicartefact_id)
        if artefact and artefact.account == performing_account:
            artefact.isdeleted = True
            artefact.lastmodifieddate = datetime.now()
            self.db.commit()
            return True
        else:
            return False

    # Equivalent to the DeleteById() method from design
    def hard_delete_music_artefact(self, musicartefact_id: int, performing_account: Account) -> bool:
        """Hard delete a music artefact."""
        artefact = self.get_music_artefact(musicartefact_id)
        if performing_account.role == RoleEnum.ADMINISTRATOR or (artefact and artefact.account == performing_account):
            self.db.delete(artefact)
            self.db.commit()
            return True
        else:
            return False
        
    # Equivalent to the ModifyById() method from design
    def update_music_artefact(self, musicartefact_id: int, performing_account: Account, new_data: dict) -> Optional[MusicArtefact]:
        """Update a music artefact."""
        artefact = self.get_music_artefact(musicartefact_id)
        if artefact and artefact.account == performing_account:
            for key, value in new_data.items():
                if key == "pathtofile":  # Check if the file path is being updated
                    existing_file_path = artefact.pathtofile
                    new_file_path = value
                    FileHandler.replace_file(existing_file_path, new_file_path)
                    artefact.set_checksum(new_file_path)
                    value=existing_file_path
                setattr(artefact, key, value)
            artefact.lastmodifieddate = datetime.now()
            self.db.commit()
            return artefact
        else:
            return None

    # Equivalent to the ShowById() method from design
    def view_music_artefact(self, musicartefact_id: int) -> Optional[MusicArtefact]:
        """View a music artefact."""
        return self.get_music_artefact(musicartefact_id)

    # Equivalent to the ShowById() method from design
    def view_all_music_artefacts(self) -> List[MusicArtefact]:
        """View all music artefacts."""
        return self.db.query(MusicArtefact).filter(
            MusicArtefact.isdeleted==False
            ).all()
