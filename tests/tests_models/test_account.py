import pytest
from datetime import date
from main.models.account import Account
from main.models.login import Login
from main.models.roles import RoleEnum

# Fixtures for Account
@pytest.fixture
def sample_account():
    return Account(
        firstname="John",
        lastname="Doe",
        dateOfBirth=date(1990, 1, 1),
        email="john.doe@example.com",
        role=RoleEnum.USER
    )

@pytest.fixture
def sample_login():
    return Login(
        username="testuser",
        password="hashedpassword",
        salt="somesalt"
    )

# Test get_username method
def test_get_username_no_login(sample_account):
    """Test get_username when there is no login associated."""
    assert sample_account.get_username() is None

def test_get_username_with_login(sample_account, sample_login):
    """Test get_username when there is a login associated."""
    sample_account.login = sample_login
    assert sample_account.get_username() == "testuser"

# Test account properties
def test_account_properties(sample_account):
    """Test basic properties of the account."""
    assert sample_account.firstname == "John"
    assert sample_account.lastname == "Doe"
    assert sample_account.dateOfBirth == date(1990, 1, 1)
    assert sample_account.email == "john.doe@example.com"
    assert sample_account.role == RoleEnum.USER
