"""
TDPS Detect API :: Object Detection Endpoint
"""

import base64
import binascii
import json
import io

from sqlalchemy import exc
from flask import Blueprint, request
from flask_restplus import Resource, Api, fields
from imageio import imread

from detect import db
from detect.api.models import Material

detect_blueprint = Blueprint("detect", __name__)
api = Api(detect_blueprint)


# === Format for marshaled response objects === #
# These dictionaries act as templates for response objects
material = api.model(
    "Material",
    {
        "id": fields.Integer(readOnly=True),
        "material_id": fields.Integer(readOnly=True),
        "description": fields.String(),
        "cluster": fields.String(),
    },
)
# Custom model for the response
resource_fields = {
    "message": fields.String(),
    "cluster": fields.String(),
    "materials": fields.List(fields.Integer()),
}


def from_base64(img_string: str):
    """Converts a base64 image string to numpy uint8 image array."""
    # If base64 has metadata attached, get only data after comma
    if img_string.startswith("data"):
        img_string = img_string.split(",")[-1]

    # Convert string to array
    return imread(io.BytesIO(base64.b64decode(img_string)))


class Detect(Resource):
    @api.marshal_with(resource_fields)
    def post(self):
        post_data = request.get_json()
        img_b64 = post_data.get("imgb64")
        response_object = {}

        # Convert to imageio (numpy) array
        try:
            img = from_base64(img_b64)
        except AttributeError:
            response_object["message"] = "Input payload validation failed"
            return response_object, 400
        except binascii.Error as e:
            response_object["message"] = str(e)
            return response_object, 400
        else:
            response_object["message"] = "success"

        # TODO: Make prediction
        predicted_cluster = "plastic_containers"
        response_object["cluster"] = predicted_cluster

        # TODO: Get material_id list from database
        materials = [
            593,
            466,
            621,
            471,
            677,
        ]
        response_object["materials"] = materials

        return response_object, 201


class Clusters(Resource):
    # @api.marshal_with(material, as_list=True)
    @api.marshal_with(resource_fields)
    def get(self, cluster):
        # Instantiate response object
        response_object = {}
        response_object["cluster"] = cluster

        # Get list of records matching the cluster name
        materials = Material.query.filter(Material.cluster == cluster).all()
        if not materials:  # Query was unsuccessful
            response_object["materials"] = []
            response_object["message"] = f"No materials listed for {cluster}"
            return response_object, 404

        else:
            response_object["materials"] = [row.material_id for row in materials]
            response_object["message"] = "success"
            return response_object, 200


api.add_resource(Clusters, "/clusters/<cluster>")
api.add_resource(Detect, "/detect")
