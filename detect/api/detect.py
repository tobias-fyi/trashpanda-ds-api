"""
TDPS Detect API :: Object Detection Endpoint
"""

from flask import Blueprint
from flask_restplus import Resource, Api

detect_blueprint = Blueprint("detect", __name__)
api = Api(detect_blueprint)


class Detect(Resource):
    def get(self):
        return {
            "status": "success",
            "cluster": "plastic_containers",
            "materials": [593, 466, 621, 471, 236, 677,],
        }


api.add_resource(Detect, "/detect")
