import pytest
from fastapi.testclient import TestClient

from app.main import app as legacy_app
from src.main import backend_app

PREFIX = "/api/v1"


@pytest.fixture(scope="module", params=["legacy", "backend"])
def client(request):
    app = legacy_app if request.param == "legacy" else backend_app
    with TestClient(app) as c:
        yield c


def test_health_counts_products(client):
    body = client.get("/health").json()
    assert body["status"] == "ok"
    assert body["products"] == 3


def test_product_listing_filter_and_detail(client):
    products = client.get(f"{PREFIX}/products").json()
    assert {p["id"] for p in products} == {"sku-001", "sku-002", "sku-003"}
    tagged = client.get(f"{PREFIX}/products", params={"tag": "bags"}).json()
    assert [p["id"] for p in tagged] == ["sku-002"]
    assert client.get(f"{PREFIX}/products/sku-001").json()["title"] == "Heritage Jacket"
    assert client.get(f"{PREFIX}/products/nope").status_code == 404


def test_cart_accumulates_lines_and_subtotal(client):
    first = client.post(f"{PREFIX}/cart", json={"line": {"productId": "sku-002", "quantity": 2}}).json()
    assert first["subtotal"] == 156.0 and first["currency"] == "USD"
    second = client.post(
        f"{PREFIX}/cart",
        json={"cartId": first["cartId"], "line": {"productId": "sku-003", "quantity": 1}},
    ).json()
    assert second["cartId"] == first["cartId"]
    assert len(second["lines"]) == 2
    assert second["subtotal"] == 252.0


def test_cart_validation_errors(client):
    assert client.post(f"{PREFIX}/cart", json={"line": {"productId": "missing", "quantity": 1}}).status_code == 404
    assert client.post(f"{PREFIX}/cart", json={"line": {"productId": "sku-001", "quantity": 0}}).status_code == 422
    assert client.post(f"{PREFIX}/cart", json={"line": {"productId": "sku-001", "quantity": 21}}).status_code == 422


def test_backend_orders_checkout_integrations(monkeypatch):
    monkeypatch.delenv("STRIPE_SECRET_KEY", raising=False)
    with TestClient(backend_app) as c:
        order = c.post(
            f"{PREFIX}/orders",
            json={"email": "buyer@example.com", "items": [{"sku": "demo", "price_cents": 2500}]},
        ).json()
        assert order["total_cents"] == 2500
        assert c.get(f"{PREFIX}/orders").json()["total"] >= 1
        session = c.post(
            f"{PREFIX}/checkout/session",
            json={"amount_cents": 2500, "email": "buyer@example.com"},
        )
        assert session.status_code == 200
        assert session.json()["provider"] == "demo"
        assert c.post(f"{PREFIX}/checkout/session", json={"amount_cents": 1, "email": "x@y.co"}).status_code == 422
        assert set(c.get(f"{PREFIX}/integrations/status").json()) == {"shopify", "stripe", "shippo"}
