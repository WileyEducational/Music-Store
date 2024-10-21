import pytest
from sqlalchemy.orm import Session
from unittest.mock import MagicMock, patch
from main.models.account import Account
from main.models.login import Login
from main.models.roles import RoleEnum
from main.controllers.account_controller import AccountController

# Fixtures for AccountController
@pytest.fixture
def mock_db_session():
    return MagicMock(spec=Session)

@pytest.fixture
def account_controller(mock_db_session):
    return AccountController(mock_db_session)

# Fixtures for sample data
@pytest.fixture
def sample_account():
    return Account(
        firstname="John",
        lastname="Doe",
        dateOfBirth="1990-01-01",
        email="john.doe@example.com",
        role=RoleEnum.USER
    )

@pytest.fixture
def sample_login(sample_account):
    return Login(
        username="johndoe",
        password="hashedpassword",
        salt="somesalt",
        account=sample_account
    )

# Test create_user_account method
@patch('main.controllers.account_controller.Login.validate_password')
@patch('main.controllers.account_controller.Login.generate_salt')
@patch('main.controllers.account_controller.Login.hash_password')
def test_create_user_account(mock_hash_password, mock_generate_salt, mock_validate_password, account_controller, mock_db_session):
    """Test creating a user account."""
    mock_validate_password.return_value = True
    mock_generate_salt.return_value = b'somesalt'  # Corrected salt value
    mock_hash_password.return_value = "hashedpassword"

    new_account = account_controller.create_user_account(
        firstname="John",
        lastname="Doe",
        dateOfBirth="1990-01-01",
        email="john.doe@example.com",
        username="johndoe",
        password="SecureP@ssword1"
    )

    assert new_account.firstname == "John"
    assert new_account.lastname == "Doe"
    assert new_account.dateOfBirth == "1990-01-01"
    assert new_account.email == "john.doe@example.com"
    assert new_account.role == RoleEnum.USER

    mock_db_session.add.assert_any_call(new_account)
    mock_db_session.commit.assert_called_once()

# Test create_user_account method with invalid password
@patch('main.controllers.account_controller.Login.validate_password')
def test_create_user_account_invalid_password(mock_validate_password, account_controller):
    """Test creating a user account with invalid password."""
    mock_validate_password.return_value = False

    with pytest.raises(ValueError, match="Password does not meet the password policy requirements."):
        account_controller.create_user_account(
            firstname="John",
            lastname="Doe",
            dateOfBirth="1990-01-01",
            email="john.doe@example.com",
            username="johndoe",
            password="weakpassword"
        )

# Test get_user_by_username method
def test_get_user_by_username(account_controller, mock_db_session, sample_login):
    """Test retrieving a user by username."""
    mock_db_session.query().filter().first.return_value = sample_login

    account = account_controller.get_user_by_username("johndoe")
    assert account == sample_login.account

    mock_db_session.query().filter().first.return_value = None
    account = account_controller.get_user_by_username("nonexistentuser")
    assert account is None

# Test get_user_by_email method
def test_get_user_by_email(account_controller, mock_db_session, sample_account):
    """Test retrieving a user by email."""
    mock_db_session.query().filter().first.return_value = sample_account

    account = account_controller.get_user_by_email("john.doe@example.com")
    assert account == sample_account

    mock_db_session.query().filter().first.return_value = None
    account = account_controller.get_user_by_email("nonexistent@example.com")
    assert account is None
