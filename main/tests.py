from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient


class TestAdminView:
    def test_login_view(self):
        client = APIClient()
        resp = client.get(reverse('admin:login'))
        assert resp.status_code == status.HTTP_200_OK

    def test_without_auth(self):
        client = APIClient()
        resp = client.get(reverse('admin:index'))
        assert resp.status_code == status.HTTP_302_FOUND

    def test_with_auth(self):
        client = APIClient()
        client.force_authenticate(user='root')
        resp = client.get(reverse('admin:index'))
        assert resp.status_code == status.HTTP_302_FOUND
