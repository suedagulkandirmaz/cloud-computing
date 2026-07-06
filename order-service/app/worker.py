import json
import time

from app.logger import logger
from app.queue.producer import fake_queue
from app.database import SessionLocal
from app.models import Order


def process_orders():

    logger.info("Worker started and waiting for messages...")

    while True:

        if fake_queue:

            message = fake_queue.pop(0)

            data = json.loads(message)

            order_id = data["order_id"]

            db = SessionLocal()

            order = db.query(Order).filter(Order.id == order_id).first()

            if order:

                order.status = "PROCESSING"
                db.commit()

                logger.info(f"Processing order {order_id}")

                time.sleep(5)

                order.status = "COMPLETED"
                db.commit()

                logger.info(f"Order {order_id} completed")

            db.close()

        time.sleep(1)


if __name__ == "__main__":
    process_orders()