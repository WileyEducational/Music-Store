import pytest
import bcrypt
from main.models.login import Login

# Fixtures
@pytest.fixture
def sample_password():
    return "SecureP@ssword123"

@pytest.fixture
def sample_username():
    return "testuser"

@pytest.fixture
def sample_salt():
    return bcrypt.gensalt().decode('utf-8')

@pytest.fixture
def hashed_password(sample_password, sample_salt):
    return Login.hash_password(sample_password, sample_salt)

# Tests for hash_password
def test_hash_password(sample_password, sample_salt):
    hashed = Login.hash_password(sample_password, sample_salt)
    assert bcrypt.checkpw(sample_password.encode('utf-8'), hashed.encode('utf-8'))

# Tests for verify_password
def test_verify_password(sample_password, hashed_password):
    assert Login.verify_password(sample_password, hashed_password)

def test_verify_password_wrong_password(sample_password, hashed_password):
    wrong_password = "WrongPassword123"
    assert not Login.verify_password(wrong_password, hashed_password)

# Tests for generate_salt
def test_generate_salt():
    salt = Login.generate_salt()
    assert isinstance(salt, str)
    assert bcrypt.gensalt().decode('utf-8')  # Ensure the salt can be generated

# Tests for validate_password
def test_validate_password_valid(sample_username):
    valid_password = "ValidP@ss123"
    assert Login.validate_password(sample_username, valid_password)

def test_validate_password_too_short(sample_username):
    short_password = "Short1!"
    assert not Login.validate_password(sample_username, short_password)

def test_validate_password_too_long(sample_username):
    long_password = "A" * 65 + "1!"
    assert not Login.validate_password(sample_username, long_password)

def test_validate_password_contains_username(sample_username):
    password_with_username = "testuserP@ss123"
    assert not Login.validate_password(sample_username, password_with_username)

def test_validate_password_common_word(sample_username):
    common_password = "Password1!"
    assert not Login.validate_password(sample_username, common_password)

def test_validate_password_no_uppercase(sample_username):
    no_uppercase = "nouppercase1!"
    assert not Login.validate_password(sample_username, no_uppercase)

def test_validate_password_no_lowercase(sample_username):
    no_lowercase = "NOLOWERCASE1!"
    assert not Login.validate_password(sample_username, no_lowercase)

def test_validate_password_no_digit(sample_username):
    no_digit = "NoDigit!"
    assert not Login.validate_password(sample_username, no_digit)

def test_validate_password_no_special_char(sample_username):
    no_special_char = "NoSpecialChar1"
    assert not Login.validate_password(sample_username, no_special_char)