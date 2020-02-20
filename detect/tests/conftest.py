"""
TPDS Detect API :: Pytest Fixtures
"""

import csv

import pytest

from detect import create_app, db
from detect.api.models import Material


@pytest.fixture(scope="module")
def test_app():
    app = create_app()
    app.config.from_object("detect.config.TestingConfig")
    with app.app_context():
        yield app  # Testing happens here


@pytest.fixture(scope="module")
def test_database():
    db.create_all()
    # Add data to db
    with open("detect/db/materials.csv", "r") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            material = Material(
                material_id=int(row[0]), description=row[1], cluster=row[2],
            )
            db.session.add(material)
    db.session.commit()  # Commit the new changes

    yield db  # Testing happens here

    db.session.remove()
    db.drop_all()
