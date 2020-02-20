"""
TPDS Detect API :: Endpoint Test `/detect`
"""

import json


def test_detect(test_app):
    """Tests the `/detect` API endpoint."""
    # Make request and parse the response
    client = test_app.test_client()
    resp = client.get("/detect")
    data = json.loads(resp.data.decode())
    # Test the response
    assert resp.status_code == 200
    assert "plastic_containers" in data["cluster"]
    assert "success" in data["status"]
    assert len(data["materials"]) > 0
