from datetime import datetime, timezone
from uuid import uuid4

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/orders", tags=["orders"])
_ORDERS: list[dict] = []


class OrderCreate(BaseModel):
    email: str
    items: list[dict]


@router.get("")
def list_orders():
    return {"items": _ORDERS, "total": len(_ORDERS)}


@router.post("")
def create_order(body: OrderCreate):
    row = {
        "id": str(uuid4()),
        "status": "paid",
        "total_cents": sum(int(i.get("price_cents", 0)) for i in body.items),
        "created_at": datetime.now(timezone.utc).isoformat(),
        **body.model_dump(),
    }
    _ORDERS.append(row)
    return row
