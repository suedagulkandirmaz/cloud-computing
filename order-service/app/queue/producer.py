import json

fake_queue = []

def send_to_queue(order_id: int):
    message = json.dumps({
        "order_id": order_id
    })

    fake_queue.append(message)
    print("Sent to queue:", message)