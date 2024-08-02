from django.db import models
from django.urls import reverse
from commons.models import TimeStampedModel
from commons.choice_helper import CATEGORY_CHOICES

class Category(TimeStampedModel):
    name = models.CharField(max_length=255, choices=CATEGORY_CHOICES, unique=True)
    
    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Categories'
        
    def __str__(self) -> str:
        return self.name
    
    def get_absolute_url(self):
        return reverse('category-detail', kwargs={'pk': self.id})