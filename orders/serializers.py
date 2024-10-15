from rest_framework import serializers
from orders.models import Order, OrderItem
from carts.models import CartItem
from store.models import Product

class OrderItemSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'price']

class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, read_only=True)
    reference = serializers.CharField(read_only=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    total_amount = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    order_status = serializers.CharField(read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'reference', 'user', 'order_items', 'total_amount', 'paid', 'order_status', 'created_at']

    def create(self, validated_data):
        user = validated_data['user']
        
        # Check if there is an existing order with 'pending' status
        existing_order = Order.objects.filter(user=user, paid=False).first()
        
        if existing_order:
            return existing_order  # Return the existing unpaid order

        # If no existing unpaid order, proceed with creating a new one
        cart_items = CartItem.objects.filter(cart__user=user)

        if not cart_items.exists():
            raise serializers.ValidationError("Cart is empty.")

        # Create a new order and set reference
        order = Order.objects.create(user=user, reference=self.generate_reference())

        total_amount = 0
        # Create order items from cart items
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )
            total_amount += item.product.price * item.quantity

        # Set the total amount
        order.total_amount = total_amount
        order.save()

        # Clear cart after order creation
        cart_items.delete()

        return order

    def generate_reference(self):
        import uuid
        return str(uuid.uuid4())
