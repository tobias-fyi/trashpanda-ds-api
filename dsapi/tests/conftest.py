"""
TPDS API :: Pytest Fixtures
"""

import pytest

from dsapi import app, db


@pytest.fixture(scope="module")
def test_app():
    app.config.from_object("project.config.TestingConfig")
    with app.app_context():
        yield app  # Testing happens here


@pytest.fixture(scope="module")
def test_database():
    db.create_all()
    yield db  # Testing happens here
    db.session.remove()
    db.drop_all()
