"""
TPDS API :: Base endpoint configuration
"""

import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# === Instantiate the database === #
db = SQLAlchemy()


def create_app(script_info=None):

    # === Instantiate the app === #
    app = Flask(__name__)

    # === Set config === #
    app_settings = os.getenv("APP_SETTINGS")
    app.config.from_object(app_settings)

    # Set up extensions
    db.init_app(app)

    # Register blueprints
    from detect.api.detect import detect_blueprint

    app.register_blueprint(detect_blueprint)

    # Shell context for flask cli
    @app.shell_context_processor
    def ctx():
        return {"app": app, "db": db}

    return app
