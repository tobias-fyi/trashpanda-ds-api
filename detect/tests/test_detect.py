"""
TPDS Detect API :: Endpoint Test `/detect`
"""

import json

from detect import db
from detect.api.models import Material

# Load base64 string from file
test_b64 = "detect/tests/images/img_b64.txt"

with open(test_b64, "r") as f:
    img_string = f.read()


def test_detect(test_app, test_database):
    """Tests the `/detect` API endpoint with base64 string."""
    # Make request and parse the response
    client = test_app.test_client()
    resp = client.post(
        "/detect",
        data=json.dumps({"imgb64": img_string}),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    # Test the response
    assert resp.status_code == 201


def test_detect_invalid_json(test_app, test_database):
    """Test case for invalid json request."""
    client = test_app.test_client()
    resp = client.post("detect", data=json.dumps({}), content_type="application/json",)
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert "Input payload validation failed" in data["message"]


def test_detect_invalid_json_keys(test_app, test_database):
    """Test case for invalid json key in request."""
    client = test_app.test_client()
    resp = client.post(
        "detect",
        data=json.dumps({"b64_img": img_string}),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert "Input payload validation failed" in data["message"]


def test_invalid_base64_string(test_app, test_database):
    """Test case for invalid base64 image string in request."""
    client = test_app.test_client()
    resp = client.post(
        "detect",
        data=json.dumps({"imgb64": "img_string"}),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert "Invalid base64-encoded string" in data["message"]


def test_single_cluster(test_app, test_database):
    """Test case for querying for a single cluster."""
    client = test_app.test_client()
    resp = client.get("/clusters/batteries")
    # Parse the response
    data = json.loads(resp.data.decode())
    assert resp.status_code == 200
    assert len(data["materials"]) == 13
