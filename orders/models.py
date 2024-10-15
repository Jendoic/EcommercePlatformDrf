import uuid
from django.db import models
from django.db.models import Sum, F
from django.urls import reverse



from carts.models import Cart
from auths.models import CustomUser as User
from store.models import Product
from commons.models import TimeStampedModel
from commons.choice_helper import ORDER_STATUS_CHOICES



class Order(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reference = models.CharField(max_length=100, unique=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Total amount for the order
    paid = models.BooleanField(default=False)
    order_status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='pending')  # Order status
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.reference}"

class OrderItem(TimeStampedModel):
    order = models.ForeignKey(Order, related_name="order_items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Product price at the time of order

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"


    
    
   
    
