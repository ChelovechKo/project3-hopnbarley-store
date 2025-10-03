import pytest
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_products_public_list() -> None:
    client = APIClient()
    r = client.get("/api/products/")
    assert r.status_code == 200


@pytest.mark.django_db
def test_orders_requires_jwt() -> None:
    client = APIClient()
    r = client.get("/api/orders/")
    assert r.status_code in (401, 403)
