import pytest
from datetime import datetime
from unittest.mock import patch
from main.models.musicartefact import MusicArtefact
from main.models.artefacttypes import MusicArtefactType
from main.models.account import Account

# Fixtures for MusicArtefact
@pytest.fixture
def sample_account():
    return Account(
        firstname="John",
        lastname="Doe",
        dateOfBirth=datetime(1990, 1, 1),
        email="john.doe@example.com",
        role="USER"
    )

@pytest.fixture
def sample_music_artefact(sample_account):
    return MusicArtefact(
        pathtofile="/path/to/file.txt",
        artefact_type=MusicArtefactType.LYRICS,
        ownedby_id=1,
        account=sample_account,
        checksum="1234567890abcdef",
        isdeleted=False
    )

# Test MusicArtefact properties
def test_music_artefact_properties(sample_music_artefact):
    """Test basic properties of the music artefact."""
    assert sample_music_artefact.pathtofile == "/path/to/file.txt"
    assert sample_music_artefact.artefact_type == MusicArtefactType.LYRICS
    assert sample_music_artefact.checksum == "1234567890abcdef"
    assert sample_music_artefact.isdeleted == False

# Test calculate_checksum method
@patch('main.models.musicartefact.ChecksumUtility.calculate_checksum')
def test_calculate_checksum(mock_calculate_checksum, sample_music_artefact):
    """Test the calculation of the checksum."""
    mock_calculate_checksum.return_value = "abcdef1234567890"
    checksum = sample_music_artefact.calculate_checksum("/path/to/file.txt")
    assert checksum == "abcdef1234567890"
    mock_calculate_checksum.assert_called_once_with("/path/to/file.txt")

# Test set_checksum method
@patch('main.models.musicartefact.ChecksumUtility.calculate_checksum')
def test_set_checksum(mock_calculate_checksum, sample_music_artefact):
    """Test setting the checksum."""
    mock_calculate_checksum.return_value = "abcdef1234567890"
    sample_music_artefact.set_checksum("/path/to/file.txt")
    assert sample_music_artefact.checksum == "abcdef1234567890"
    mock_calculate_checksum.assert_called_once_with("/path/to/file.txt")

# Test print_details method
@patch('builtins.print')
def test_print_details(mock_print, sample_music_artefact, sample_account):
    """Test the print details method."""
    sample_account.get_username = lambda: "testuser"
    sample_music_artefact.print_details()
    mock_print.assert_any_call()
    mock_print.assert_any_call(f"MusicArtefact ID: {sample_music_artefact.musicartefactid}")
    mock_print.assert_any_call(f"Owner Name: testuser")
    mock_print.assert_any_call(f"Type: {sample_music_artefact.artefact_type}")
    mock_print.assert_any_call(f"Path: {sample_music_artefact.pathtofile}")
    mock_print.assert_any_call(f"checksum: {sample_music_artefact.checksum}")
    mock_print.assert_any_call()

# Test relationship with Account
def test_music_artefact_account_relationship(sample_music_artefact, sample_account):
    """Test the relationship between MusicArtefact and Account."""
    assert sample_music_artefact.account == sample_account
    assert sample_music_artefact in sample_account.music_artefacts
