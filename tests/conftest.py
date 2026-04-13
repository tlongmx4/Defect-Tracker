from dotenv import load_dotenv
load_dotenv()

import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
from app.db.base import Base

TEST_DATABASE_URL = os.environ["TEST_DATABASE_URL"]

test_engine = create_engine(
    TEST_DATABASE_URL,
    pool_pre_ping=True
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

@pytest.fixture(scope="session")
def setup_schema():
    Base.metadata.create_all(bind=test_engine)
    yield

@pytest.fixture()
def setup_session(setup_schema):
    connection = test_engine.connect()
    trans = connection.begin()
    session = Session(
            bind=connection, join_transaction_mode="create_savepoint"
        ) 
    yield session
    session.close()
    trans.rollback()
    connection.close()




