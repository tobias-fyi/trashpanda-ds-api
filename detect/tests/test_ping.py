"""
TPDS Detect API :: Endpoint Test `/ping`
"""

import json


def test_ping(test_app):
    """Tests the `/ping` API endpoint."""
    # Make request and parse the response
    client = test_app.test_client()
    resp = client.get("/ping")
    data = json.loads(resp.data.decode())
    # Test the response
    assert resp.status_code == 200
    assert "pong" in data["message"]
    assert "success" in data["status"]
