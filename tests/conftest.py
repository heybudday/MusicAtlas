import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.models.base import Base

import app.models


@pytest.fixture
def db_session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(engine)