from fastapi import APIRouter

from src.services.catalog import CartRequest, upsert_cart

router = APIRouter(prefix="/cart", tags=["cart"])


@router.post("")
def cart(body: CartRequest) -> dict:
    return upsert_cart(body)
