from fastapi import APIRouter

from src.services.catalog import PRODUCTS

router = APIRouter(tags=["health"])


@router.get("/health")
def health() -> dict:
    return {"status": "ok", "products": len(PRODUCTS)}
