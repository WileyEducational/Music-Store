from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Enum
from sqlalchemy.orm import relationship
from ..database import Base
from ..utilities.Checksum import ChecksumUtility
from .artefacttypes import MusicArtefactType

class MusicArtefact(Base):   
    __tablename__ = 'musicartefact'
    
    musicartefactid = Column(Integer, primary_key=True, index=True)
    isdeleted = Column(Boolean, default=False)
    creationdate = Column(DateTime, default=datetime.now, nullable=False)
    lastmodifieddate = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)
    checksum = Column(String, nullable=False)
    pathtofile = Column(String, nullable=False)
    artefact_type = Column(Enum(MusicArtefactType), nullable=False)

    ownedby_id = Column(Integer, ForeignKey('accounts.id'), nullable=False)
    account = relationship("Account", back_populates="music_artefacts", uselist=False)

    def calculate_checksum(self, file_path: str) -> str:
        """Calculate checksum of the artefact file."""
        return ChecksumUtility.calculate_checksum(file_path)

    def set_checksum(self, file_path: str) -> None:
        """Set the checksum for the artefact."""
        self.checksum = self.calculate_checksum(file_path)
        
    def print_details(self):
        print()
        print(f"MusicArtefact ID: {self.musicartefactid}")
        print(f"Owner Name: {self.account.get_username()}")
        print(f"Type: {self.artefact_type}")
        print(f"Path: {self.pathtofile}")
        print(f"checksum: {self.checksum}")
        print()
