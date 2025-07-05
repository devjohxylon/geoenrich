# type: ignore

from geoenrich import enrich\_ip, enrich\_coords

class DummyResponse:
def **init**(self, json\_data):
self.\_json = json\_data

```
def json(self):
    return self._json
```

def test\_enrich\_ip(monkeypatch):
monkeypatch.setattr(
'geoenrich.requests.Session.get',
lambda self, url, \*\*kwargs: DummyResponse({
'country\_name': 'United States',
'region': 'NY',
'city': 'NYC',
'latitude': 40.7,
'longitude': -74.0,
})
)
data = enrich\_ip('8.8.8.8', timeout=5, retries=2)
assert data\['ip\_country'] == 'United States'
assert data\['ip\_lat']     == 40.7
assert data\['ip\_lng']     == -74.0

def test\_enrich\_coords(monkeypatch):
dummy\_payload = {
'results': \[
{
'components': {'country': 'United States', 'state': 'NY', 'city': 'NYC'},
'geometry': {'lat': 40.7, 'lng': -74.0},
}
]
}
monkeypatch.setattr(
'geoenrich.requests.Session.get',
lambda self, url, \*\*kwargs: DummyResponse(dummy\_payload)
)
data = enrich\_coords(40.7128, -74.0060, timeout=5, retries=2)
assert data\['geo\_country'] == 'United States'
assert data\['geo\_city']    == 'NYC'
assert data\['geo\_lat']     == 40.7
assert data\['geo\_lng']     == -74.0
# This code is a test suite for the geoenrich module, which enriches IP addresses and geographic coordinates with location data.