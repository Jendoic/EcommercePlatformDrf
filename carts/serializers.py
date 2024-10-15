from rest_framework import serializers
from store.models import Product
from carts.models import Cart, CartItem
from orders.models import Order, OrderItem
from store.serializers import ProductSerializer



# Created specifically for CartItem operations only. not to be used on views.
class SimpleProductserializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price']


class CartItemSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    sub_total = serializers.SerializerMethodField(method_name="get_sub_total")

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'sub_total']  # 'cart' removed as the issue was resolved

    def get_sub_total(self, cartitem: CartItem):
        return cartitem.product.price * cartitem.quantity



class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    cart_items = CartItemSerializer(many=True, source='items')  # Assuming cartitem_set is the related name
    grand_total = serializers.SerializerMethodField(method_name='get_grand_total_amount')

    class Meta:
        model = Cart
        fields = ['id', 'user', 'cart_items', 'grand_total']  # Add 'cart_items' to the fields list

    def get_grand_total_amount(self, cart: Cart):
        # Calculate the total by iterating through cart items and computing subtotals
        cart_items = CartItem.objects.filter(cart=cart)
        total_amount = sum([item.product.price * item.quantity for item in cart_items])
        return total_amount
