"""
TPDS API :: Base endpoint configuration
"""

import os
from flask import Flask, jsonify
from flask_restplus import Resource, Api
from flask_sqlalchemy import SQLAlchemy

# === Instantiate the app === #
app = Flask(__name__)

# === Instantiate the API === #
api = Api(app)

# === Set config === #
app_settings = os.getenv("APP_SETTINGS")
app.config.from_object("dsapi.config.DevelopmentConfig")

# === Instantiate the database === #
db = SQLAlchemy(app)

# === Data model === #
class Material(db.Model):
    __tablename__ = "materials"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    material_id = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(64), nullable=False)
    cluster = db.Column(db.String(64))

    def __init__(self, material_id, description, cluster):
        self.material_id = material_id
        self.description = description
        self.cluster = cluster


class Ping(Resource):
    def get(self):
        return {
            "status": "success",
            "message": "pong!",
        }


api.add_resource(Ping, "/ping")
