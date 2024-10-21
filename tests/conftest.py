import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main.database import Base

DATABASE_URL = "sqlite:///test_database.db"

@pytest.fixture(scope='session')
def engine():
    return create_engine(DATABASE_URL, echo=True)

@pytest.fixture(scope='session')
def tables(engine):
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope='session')
def db_session(engine, tables):
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()

@pytest.fixture(scope='session', autouse=True)
def remove_test_db_file(request):
    """Remove the test database file after tests."""
    def cleanup():
        if os.path.exists("test_database.db"):
            os.remove("test_database.db")
    request.addfinalizer(cleanup)
