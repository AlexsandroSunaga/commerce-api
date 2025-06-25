import os

from fastapi import APIRouter

router = APIRouter(prefix="/integrations", tags=["integrations"])


@router.get("/status")
def integration_status():
    return {
        "shopify": {"enabled": bool(os.getenv("SHOPIFY_STORE_DOMAIN"))},
        "stripe": {"enabled": bool(os.getenv("STRIPE_SECRET_KEY"))},
        "shippo": {"enabled": bool(os.getenv("SHIPPO_API_KEY"))},
    }
