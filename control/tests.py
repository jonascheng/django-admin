from rest_framework.reverse import reverse
from rest_framework.test import APIClient


class TestHealthCheck:
    def test_health_check(self):
        client = APIClient()
        resp = client.get(reverse('health-check'))
        assert resp.json() == {'success': True}
