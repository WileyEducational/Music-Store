import os
import shutil
import tempfile
import pytest
from unittest.mock import MagicMock
from main.controllers.musicartefact_controller import MusicArtefactController
from main.models.account import Account
from main.models.musicartefact import MusicArtefact
from main.models.artefacttypes import MusicArtefactType
from main.models.roles import RoleEnum

@pytest.fixture
def mock_db_session():
    return MagicMock()

@pytest.fixture
def controller(mock_db_session):
    return MusicArtefactController(mock_db_session)

@pytest.fixture
def temp_files():
    temp_dir = tempfile.mkdtemp()
    temp_txt = os.path.join(temp_dir, "test.txt")
    temp_mp3 = os.path.join(temp_dir, "test.mp3")
    
    # Create temporary text and mp3 files
    with open(temp_txt, "w") as txt_file:
        txt_file.write("Temporary text file for testing")
    with open(temp_mp3, "wb") as mp3_file:
        # Write some bytes for the mp3 file
        mp3_file.write(b"Fake MP3 content for testing")

    yield temp_txt, temp_mp3

    # Clean up the temporary directory and files
     # Clean up the temporary files and directory
    os.remove(temp_txt)
    os.remove(temp_mp3)
    os.rmdir(temp_dir)

def test_create_music_artefact_admin(controller, temp_files):
    # Unpack the temp files tuple
    temp_txt, temp_mp3 = temp_files

    performing_account = Account(role=RoleEnum.ADMINISTRATOR)
    artefact_type = MusicArtefactType.RECORDING

    new_artefact, uploaded_file_path = controller.create_music_artefact(
        performing_account,
        temp_mp3,
        artefact_type=artefact_type
    )

    assert isinstance(new_artefact, MusicArtefact)
    assert new_artefact.pathtofile == uploaded_file_path

def test_create_music_artefact_user(controller, temp_files):
    temp_txt, temp_mp3 = temp_files

    performing_account = Account(role=RoleEnum.USER)
    artefact_type = MusicArtefactType.LYRICS

    new_artefact, uploaded_file_path = controller.create_music_artefact(
        performing_account,
        temp_txt,
        artefact_type=artefact_type
    )

    assert isinstance(new_artefact, MusicArtefact)
    assert new_artefact.pathtofile == uploaded_file_path

def test_get_music_artefact(controller):
    musicartefact_id = 1
    controller.get_music_artefact = MagicMock(return_value=None)
    
    assert controller.get_music_artefact(musicartefact_id) == None

def test_soft_delete_music_artefact(controller):
    musicartefact_id = 1
    performing_account = Account(role=RoleEnum.USER)
    musicartefact = MusicArtefact(isdeleted=False, account=performing_account)

    controller.get_music_artefact = MagicMock(return_value=musicartefact)
    controller.db.commit = MagicMock()

    assert controller.soft_delete_music_artefact(musicartefact_id, performing_account) == True

def test_hard_delete_music_artefact(controller):
    musicartefact_id = 1
    performing_account = Account(role=RoleEnum.ADMINISTRATOR)
    musicartefact = MusicArtefact(isdeleted=False, account=performing_account)

    controller.get_music_artefact = MagicMock(return_value=musicartefact)
    controller.db.delete = MagicMock()
    controller.db.commit = MagicMock()

    assert controller.hard_delete_music_artefact(musicartefact_id, performing_account) == True

def test_update_music_artefact(controller):
    musicartefact_id = 1
    performing_account = Account(role=RoleEnum.USER)
    new_data = {"title": "New Title"}

    musicartefact = MusicArtefact(isdeleted=False, account=performing_account)

    controller.get_music_artefact = MagicMock(return_value=musicartefact)
    controller.db.commit = MagicMock()

    updated_artefact = controller.update_music_artefact(musicartefact_id, performing_account, new_data)

    assert updated_artefact.title == "New Title"

def test_view_music_artefact(controller):
    musicartefact_id = 1
    musicartefact = MusicArtefact(isdeleted=False)

    controller.get_music_artefact = MagicMock(return_value=musicartefact)

    assert controller.view_music_artefact(musicartefact_id) == musicartefact

def test_view_all_music_artefacts(controller):
    musicartefacts = [MusicArtefact(isdeleted=False) for _ in range(5)]

    controller.db.query.return_value.filter.return_value.all.return_value = musicartefacts

    assert len(controller.view_all_music_artefacts()) == 5

