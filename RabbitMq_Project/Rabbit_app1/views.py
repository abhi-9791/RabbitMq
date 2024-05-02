from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Order
import pika

@csrf_exempt
def create_order(request):
    if request.method == 'POST':
        data = request.POST
        order = Order.objects.create(
            customer_name=data['customer_name'],
            total_amount=data['total_amount']
        )
        publish_order_confirmation(order.order_id)
        return JsonResponse({'order_id': order.order_id})
    return JsonResponse({'error': 'Method not allowed'}, status=405)
def publish_order_confirmation(order_id):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='order_confirmation_queue')
    channel.basic_publish(exchange='', routing_key='order_confirmation_queue', body=str(order_id))
    print("Order Confirmation Published:", order_id)
    connection.close()
