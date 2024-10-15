from django.contrib import admin

from .models import Cart, CartItem

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user','session','created_at')
    search_fields = ('user', 'created_at')
    

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity', 'created_at')
    search_fields = ('cart', 'product', 'quantity', 'created_at')
    
    