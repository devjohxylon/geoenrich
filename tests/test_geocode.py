from geoenrich import enrich_ip, enrich_coords
import geoenrich


class DummyResponse:
    def __init__(self, json_data):
        self._json = json_data

    def json(self):
        return self._json

    def raise_for_status(self):
        return None  # simulate HTTP 200


def test_enrich_ip(monkeypatch):
    # Override module‐level API key
    monkeypatch.setattr(geoenrich, "OPENCAGE_KEY", "dummy")

    # Mock the HTTP call
    monkeypatch.setattr(
        "geoenrich.requests.Session.get",
        lambda self, url, **kwargs: DummyResponse(
            {
                "country_name": "United States",
                "region": "NY",
                "city": "NYC",
                "latitude": 40.7,
                "longitude": -74.0,
            }
        ),
    )

    data = enrich_ip("8.8.8.8", timeout=5, retries=2)
    assert data["ip_country"] == "United States"
    assert data["ip_lat"] == 40.7
    assert data["ip_lng"] == -74.0


def test_enrich_coords(monkeypatch):
    # Override module‐level API key
    monkeypatch.setattr(geoenrich, "OPENCAGE_KEY", "dummy")

    dummy_payload = {
        "results": [
            {
                "components": {
                    "country": "United States",
                    "state": "NY",
                    "city": "NYC",
                },
                "geometry": {"lat": 40.7, "lng": 40.7},
            }
        ]
    }
    monkeypatch.setattr(
        "geoenrich.requests.Session.get",
        lambda self, url, **kwargs: DummyResponse(dummy_payload),
    )

    data = enrich_coords(40.7128, -74.0060, timeout=5, retries=2)
    assert data["geo_country"] == "United States"
    assert data["geo_city"] == "NYC"
    assert data["geo_lat"] == 40.7
    assert data["geo_lng"] == 40.7
