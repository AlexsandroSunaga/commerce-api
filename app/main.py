import json
import uuid
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

DATA = Path(__file__).resolve().parent.parent / "data" / "products.json"
PRODUCTS = json.loads(DATA.read_text(encoding="utf-8"))
CARTS: dict[str, list[dict]] = {}

app = FastAPI(title="Storefront API", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "products": len(PRODUCTS)}


@app.get("/api/v1/products")
def list_products(tag: str | None = None) -> list[dict]:
    if not tag:
        return PRODUCTS
    return [p for p in PRODUCTS if tag in p.get("tags", [])]


@app.get("/api/v1/products/{product_id}")
def get_product(product_id: str) -> dict:
    for p in PRODUCTS:
        if p["id"] == product_id:
            return p
    raise HTTPException(404, "Product not found")


class CartLine(BaseModel):
    productId: str
    quantity: int = Field(ge=1, le=20)


class CartRequest(BaseModel):
    cartId: str | None = None
    line: CartLine


@app.post("/api/v1/cart")
def upsert_cart(body: CartRequest) -> dict:
    cart_id = body.cartId or str(uuid.uuid4())
    product = next((p for p in PRODUCTS if p["id"] == body.line.productId), None)
    if not product:
        raise HTTPException(404, "Product not found")
    lines = CARTS.setdefault(cart_id, [])
    lines.append({"productId": product["id"], "quantity": body.line.quantity, "unitPrice": product["price"]})
    subtotal = sum(l["quantity"] * l["unitPrice"] for l in lines)
    return {"cartId": cart_id, "lines": lines, "subtotal": round(subtotal, 2), "currency": product["currency"]}
