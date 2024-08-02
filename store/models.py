from django.db import models
from django.urls import reverse
from categories.models import Category
from commons.models import TimeStampedModel


class Product(TimeStampedModel):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    is_available = models.BooleanField(default=True)
    
    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Products'
    
    def __str__(self) -> str:
        return self.name
    
    def get_absolute_url(self) -> str:
        return reverse('product-detail', kwargs={'pk': self.id})
    
    def save(self,*args, **kwargs):
        if self.stock <= 0:
            self.is_available = False
        else:
            self.is_available = True
        super().save(*args, **kwargs)