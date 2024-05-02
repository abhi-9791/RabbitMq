from flask import Flask
from celery import Celery
from flask import request
import pika

app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = 'amqp://guest:guest@localhost'
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])

@app.route('/order-confirmation', methods=['POST'])
def handle_order_confirmation():
    order_id = request.get_data(as_text=True)
    send_order_confirmation_email.delay(order_id)
    return 'Order confirmation sent'

@celery.task
def send_order_confirmation_email(order_id):
    order = Order.objects.get(order_id=order_id)
    print(f"Sending order confirmation email to {order.customer_name}")

if __name__ == '__main__':
    app.run(debug=True)