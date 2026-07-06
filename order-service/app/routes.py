from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import Order
from app.schemas import OrderCreate, OrderUpdate, LoginRequest
from app.auth import (
    get_current_user,
    authenticate_user,
    create_access_token
)
from app.queue.producer import send_to_queue
from app.logger import logger

router = APIRouter()


# -----------------------------
# Database
# -----------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -----------------------------
# Login
# -----------------------------
@router.post("/login")
def login(user: LoginRequest):

    if not authenticate_user(user.username, user.password):
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    token = create_access_token({
        "sub": user.username
    })

    logger.info(f"User {user.username} logged in")

    return {
        "access_token": token,
        "token_type": "bearer"
    }


# -----------------------------
# Create Order
# -----------------------------
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

    logger.info(f"Order {new_order.id} created")

    send_to_queue(new_order.id)

    return {
        "message": "Order queued",
        "order_id": new_order.id,
        "status": new_order.status,
        "total_price": new_order.total_price
    }


# -----------------------------
# Get All Orders
# -----------------------------
@router.get("/orders")
def get_orders(
    db: Session = Depends(get_db),
    user: str = Depends(get_current_user)
):
    return db.query(Order).all()


# -----------------------------
# Get Order By ID
# -----------------------------
@router.get("/orders/{order_id}")
def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    user: str = Depends(get_current_user)
):

    order = db.query(Order).filter(Order.id == order_id).first()

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    return order


# -----------------------------
# Update Order
# -----------------------------
@router.put("/orders/{order_id}")
def update_order(
    order_id: int,
    updated_order: OrderUpdate,
    db: Session = Depends(get_db),
    user: str = Depends(get_current_user)
):

    order = db.query(Order).filter(Order.id == order_id).first()

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    order.customer_name = updated_order.customer_name
    order.product_id = updated_order.product_id
    order.quantity = updated_order.quantity
    order.total_price = updated_order.quantity * 20

    db.commit()
    db.refresh(order)
    logger.info(f"Order {order.id} updated")

    return {
        "message": "Order updated successfully",
        "order": order
    }


# -----------------------------
# Delete Order
# -----------------------------
@router.delete("/orders/{order_id}")
def delete_order(
    order_id: int,
    db: Session = Depends(get_db),
    user: str = Depends(get_current_user)
):

    order = db.query(Order).filter(Order.id == order_id).first()

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    db.delete(order)
    db.commit()
    logger.info(f"Order {order_id} deleted")

    return {
        "message": "Order deleted successfully"
    }