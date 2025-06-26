from fastapi import APIRouter

from src.services.catalog import get_product, list_products

router = APIRouter(prefix="/products", tags=["products"])


@router.get("")
def products(tag: str | None = None) -> list[dict]:
    return list_products(tag)


@router.get("/{product_id}")
def product(product_id: str) -> dict:
    return get_product(product_id)
