import pytest
from django.urls import reverse
from context import api_client

@pytest.mark.django_db
def test_unauthorized_request(api_client):
   url = reverse('need-token-url')
   response = api_client.get(url)
   assert response.status_code == 401