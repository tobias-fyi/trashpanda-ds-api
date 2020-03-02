"""
TDPS Detect API :: Object Detection Endpoint
"""

import base64
import binascii
import json
import io
import os
import random

import cv2
from flask import Blueprint, request, redirect, url_for
from flask_restplus import Resource, Api, fields
from imageio import imread
import numpy as np
from sqlalchemy import exc

from detect import db
from detect.api.models import Material
from detect.api.yolo import get_prediction, load_model

detect_blueprint = Blueprint("detect", __name__)
api = Api(detect_blueprint)


# === YOLO config variables === #
# Paths to necessary files
yolo_path = "detect/api/yolo_config"
weights_path = os.path.join(yolo_path, "yolo-obj_7000.weights")
config_path = os.path.join(yolo_path, "yolo-obj.cfg")
classes_path = os.path.join(yolo_path, "classes.txt")
test_img_path = os.path.join(yolo_path, "032.png")
# Config vars
conf_thresh = 0.3  # Confidence threshold
nms_thresh = 0.1  # Non-maximum suppression

# === Instantiate network === #
net = load_model(config_path, weights_path)

# === Format for marshaled response objects === #
# These dictionaries act as templates for response objects
# and can validate the response if needed.
material = api.model(  # Format/validate the data model as json
    "Material",
    {
        "id": fields.Integer(readOnly=True),
        "material_id": fields.Integer(readOnly=True),
        "description": fields.String(),
        "cluster": fields.String(),
    },
)
# Format/validate custom json response
resource_fields = {
    "message": fields.String(),
    "pred_time": fields.Float(),
    "confidence": fields.Float(),
    "cluster_name": fields.String(),
    "cluster": fields.String(),
    "materials": fields.List(fields.Integer()),
}


def from_base64(img_string: str):
    """Converts a base64 image string to numpy uint8 image array."""
    # If base64 has metadata attached, get only data after comma
    if img_string.startswith("data"):
        img_string = img_string.split(",")[-1]
    # Convert string to array and load into opencv
    img_array = imread(io.BytesIO(base64.b64decode(img_string)))
    return cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)


def snake_to_cd_case(name: str):
    """Converts a snake_case cluster name to Title Case.
    In the case of 'cd_cases', abbreviation is capitalized."""
    split = name.title().split("_")
    if len(split[0]) == 2:
        split[0] = split[0].upper()
    return " ".join(split)


class Ping(Resource):
    def get(self):
        return {
            "status": "success",
            "message": "pong!",
        }


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

        # === Run object detection === #
        prediction, confidence, pred_time = get_prediction(img, net)
        response_object["cluster"] = prediction
        response_object["confidence"] = round(confidence, 4)
        response_object["pred_time"] = round(pred_time, 4)

        # Format into Title Case for display purposes
        if prediction:
            response_object["cluster_name"] = snake_to_cd_case(prediction)

            # Get list of materials for the predicted cluster
            materials = Material.query.filter(Material.cluster == prediction).all()

            if not materials:  # Query was unsuccessful
                response_object["materials"] = []
                response_object["message"] = f"No materials listed for {prediction}"
                return response_object, 404

            else:  # Query was successful
                response_object["materials"] = [row.material_id for row in materials]
                response_object["message"] = "success"
                return response_object, 200

        else:  # No prediction was made
            return response_object, 200


class Clusters(Resource):
    @api.marshal_with(resource_fields)
    def get(self, cluster):
        # Instantiate response object
        response_object = {}
        response_object["cluster"] = cluster

        # Format into Title Case for display purposes
        response_object["cluster_name"] = snake_to_cd_case(cluster)

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


class ClustersList(Resource):
    @api.marshal_with(material, as_list=True)
    def get(self):
        return Material.query.all(), 200


api.add_resource(Ping, "/ping")
api.add_resource(Detect, "/detect")
api.add_resource(ClustersList, "/clusters")
api.add_resource(Clusters, "/clusters/<cluster>")
