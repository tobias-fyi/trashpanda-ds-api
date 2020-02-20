"""
TPDS Detect API :: Flask CLI Configuration
"""

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
    db.session.commit()


if __name__ == "__main__":
    cli()
