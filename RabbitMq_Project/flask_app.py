from flask import Flask
from celery import Celery
import pika
import requests
# from flask_ import SQLAlchemy
from flask import Flask
from flask_mail import Mail,Message

app = Flask(__name__)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'abhishek.yeduru@cogentdatasolutions.in'
app.config['MAIL_PASSWORD'] = 'cudw kivw kuum itwx'

mail = Mail(app)
app.config['CELERY_BROKER_URL'] = 'amqp://guest:guest@localhost'
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///D:/RabbitMq/RabbitMq_Project/db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)
from Rabbit_app1.models import Order
@app.route('/')
def index():
    return 'Flask Notification Service is running'

@celery.task
def send_order_confirmation_email(order_id):
    order = Order.objects.get(order_id=order_id)
    print('Your order confirmed',order.customer_email)
    with app.app_context():
        msg = Message('Sending order confirmation email to', recipients=order.customer_email)
        msg.body = 'Your order confirmed'
        mail.send(msg)
    print(f"Sending order confirmation email to {order.customer_email}")

def start_rabbitmq_consumer():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='order_confirmation_queue')
    channel.basic_consume(queue='order_confirmation_queue', on_message_callback=process_order_confirmation, auto_ack=True)
    print("RabbitMQ Consumer Started...")
    channel.start_consuming()

def process_order_confirmation(ch, method, properties, body):
    print("Order Confirmation Received:", body)
    send_order_confirmation_email.delay(body)
    print("sending mail:", body)
    

if __name__ == '__main__':
    start_rabbitmq_consumer()
    app.run(debug=True)
