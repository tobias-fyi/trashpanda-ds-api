"""
TDPS Detect API :: Object Detection Endpoint
"""

import base64
import binascii
import json
import io

from flask import Blueprint, request
from flask_restplus import Resource, Api
from imageio import imread

detect_blueprint = Blueprint("detect", __name__)
api = Api(detect_blueprint)


def from_base64(img_string: str):
    """Converts a base64 image string to numpy uint8 image array."""
    # If base64 has metadata attached, get only data after comma
    if img_string.startswith("data"):
        img_string = img_string.split(",")[-1]

    # imageio array is a numpy array
    return imread(io.BytesIO(base64.b64decode(img_string)))


class Detect(Resource):
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

        # TODO: Make prediction
        predicted_cluster = "plastic_containers"

        # TODO: Get material_id list from database
        materials = [
            593,
            466,
            621,
            471,
            677,
        ]

        # Success or not (not really necessary)
        status = "success" if predicted_cluster else "fail"

        response_object = {
            "status": status,
            "cluster": predicted_cluster,
            "materials": materials,
        }

        return response_object, 201


api.add_resource(Detect, "/detect")
