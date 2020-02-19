"""
TPDS API :: Base endpoint configuration
"""

import os
from flask import Flask, jsonify
from flask_restplus import Resource, Api

# === Instantiate the app === #
app = Flask(__name__)

# === Instantiate the API === #
api = Api(app)

# === Set config === #
app_settings = os.getenv("APP_SETTINGS")
app.config.from_object("dsapi.config.DevelopmentConfig")


class Ping(Resource):
    def get(self):
        return {
            "status": "success",
            "message": "pong!",
        }


api.add_resource(Ping, "/ping")
