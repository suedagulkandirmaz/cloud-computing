from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas import OrderCreate
from app.models import Order
from app.database import SessionLocal
from app.auth import get_current_user
from app.queue.producer import send_to_queue

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/orders")
def create_order(
    order: OrderCreate,
    db: Session = Depends(get_db),
    user: str = Depends(get_current_user)
):
    total_price = order.quantity * 20

    new_order = Order(
        customer_name=order.customer_name,
        product_id=order.product_id,
        quantity=order.quantity,
        total_price=total_price,
        status="QUEUED"
    )

    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    # 🔥 QUEUE STEP (DOĞRU YER)
    send_to_queue(new_order.id)

    return {
        "message": "Order queued",
        "order_id": new_order.id
    }