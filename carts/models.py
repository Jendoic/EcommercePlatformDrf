from django.db import models
from django.db.models import Sum, F

from store.models import Product
from auths.models import CustomUser
from commons.models import TimeStampedModel


class Cart(TimeStampedModel):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    session = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Carts"
        ordering = ['-created_at']

    
    def __str__(self):
        return f"Cart #{str(self.id)}, for {self.user}"
    

    
class CartItem(TimeStampedModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Cart Items"
        ordering = ['-created_at']
    
    

    
    def __str__(self):
        return f"{self.product.name} -- {self.quantity}"