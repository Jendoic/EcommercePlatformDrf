from django.db import models
from orders.models import Order

class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)  # Link to the Order model
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10)
    status = models.CharField(max_length=20)
    transaction_id = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f"Payment for {self.order.id} - {self.status}"
