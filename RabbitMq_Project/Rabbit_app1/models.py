from django.db import models

class Order(models.Model):
    
    order_id = models.AutoField(primary_key=True)
    customer_name = models.CharField(max_length=100,null=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    is_paid = models.BooleanField(default=False)
    customer_email = models.EmailField(max_length=254,null=True)
    
