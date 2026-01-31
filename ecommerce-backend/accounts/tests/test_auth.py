from rest_framework.test import APIClient
from django.urls import reverse

def test_product_list_authenticated(user, token):
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    response = client.get(reverse("product-list"))
    assert response.status_code == 200

docker-compose run backend pytest


