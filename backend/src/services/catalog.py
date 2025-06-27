import json
import os
import uuid
from pathlib import Path

from fastapi import HTTPException
from pydantic import BaseModel, Field

# DATA_DIR overrides the default (<repo root>/data) so the Docker image can ship its own copy.
DATA_DIR = Path(os.environ.get("DATA_DIR") or Path(__file__).resolve().parents[3] / "data")
DATA_FILE = DATA_DIR / "products.json"
PRODUCTS: list[dict] = json.loads(DATA_FILE.read_text(encoding="utf-8"))
CARTS: dict[str, list[dict]] = {}


class CartLine(BaseModel):
    productId: str
    quantity: int = Field(ge=1, le=20)


class CartRequest(BaseModel):
    cartId: str | None = None
    line: CartLine


def list_products(tag: str | None = None) -> list[dict]:
    if not tag:
        return PRODUCTS
    return [p for p in PRODUCTS if tag in p.get("tags", [])]


def get_product(product_id: str) -> dict:
    for p in PRODUCTS:
        if p["id"] == product_id:
            return p
    raise HTTPException(404, "Product not found")


def upsert_cart(body: CartRequest) -> dict:
    cart_id = body.cartId or str(uuid.uuid4())
    product = next((p for p in PRODUCTS if p["id"] == body.line.productId), None)
    if not product:
        raise HTTPException(404, "Product not found")
    lines = CARTS.setdefault(cart_id, [])
    lines.append({"productId": product["id"], "quantity": body.line.quantity, "unitPrice": product["price"]})
    subtotal = sum(line["quantity"] * line["unitPrice"] for line in lines)
    return {
        "cartId": cart_id,
        "lines": lines,
        "subtotal": round(subtotal, 2),
        "currency": product["currency"],
    }
