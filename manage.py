"""
TPDS API :: Flask CLI Configuration
"""

from flask.cli import FlaskGroup

from dsapi import app


cli = FlaskGroup(app)


if __name__ == "__main__":
    cli()
