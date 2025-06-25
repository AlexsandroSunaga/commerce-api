from fastapi import APIRouter

from src.api.routes import cart, products, orders, integrations, checkout

api_router = APIRouter()
api_router.include_router(products.router)
api_router.include_router(cart.router)
api_router.include_router(orders.router)
api_router.include_router(integrations.router)
api_router.include_router(checkout.router)


