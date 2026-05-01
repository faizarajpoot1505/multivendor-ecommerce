from celery import shared_task

@shared_task
def send_order_email(order_id):
    print(f"EMAIL SENT for order {order_id}")
    return True


@shared_task
def low_stock_alert(product_name):
    print(f"LOW STOCK ALERT: {product_name}")
    return True


