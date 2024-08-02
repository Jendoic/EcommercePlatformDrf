from django.db import models

from store.models import Product
from auths.models import CustomUser
from commons.models import TimeStampedModel


class CartItem(TimeStampedModel):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Cart Items"
        ordering = ['-created_at']
    
    def subTotal_price(self):
        return self.product.price * self.quantity
    
    
    
    def __str__(self):
        return f"{self.product.name} -- {self.quantity}"