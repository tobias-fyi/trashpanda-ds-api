"""
TPDS Detect API :: Flask CLI Configuration
"""

import csv
import sys

from flask.cli import FlaskGroup

from detect import create_app, db
from detect.api.models import Material


app = create_app
cli = FlaskGroup(create_app=create_app)


@cli.command("recreate_db")
def recreate_db():
    db.drop_all()
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


if __name__ == "__main__":
    cli()
