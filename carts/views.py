

from carts.models import Cart, CartItem
from store.models import Product
from .serializers import CartSerializer, CartItemSerializer
from rest_framework import generics, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from orders.models import Order, OrderItem
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotAcceptable, ValidationError


from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Cart, CartItem, Product
from .serializers import CartSerializer, CartItemSerializer

class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    permission_classes = [AllowAny] 
    model = CartItem

    def get_queryset(self):

        user = self.request.user
        session_key = self.request.session.session_key

        if user.is_authenticated:
            return Cart.objects.filter(user=user)
        else:
            if not session_key:
                self.request.session.create()
                session_key = self.request.session.session_key
            return Cart.objects.filter(session=session_key)

    def list(self, request, *args, **kwargs):
     
        queryset = self.get_queryset()
        cart = queryset.first()

        if not cart:
            return Response({"detail": "Cart is empty."}, status=status.HTTP_200_OK)

        serializer = self.get_serializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def create(self, request, *args, **kwargs):

        serializer = CartItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = serializer.validated_data['product']
        quantity = serializer.validated_data['quantity']


        cart = self.get_queryset().first()
        if not cart:
            if request.user.is_authenticated:
                cart = Cart.objects.create(user=request.user)
            else:
                session_key = request.session.session_key
                if not session_key:
                    request.session.create()
                    session_key = request.session.session_key
                cart = Cart.objects.create(session=session_key)

        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        cart_item.quantity = quantity
        cart_item.save()


        cart_serializer = CartSerializer(cart)
        return Response(cart_serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk=None, *args, **kwargs):

        if not pk:
            return Response({"error": "Product ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        cart = self.get_queryset().first()
        if not cart:
            return Response({"error": "Cart does not exist."}, status=status.HTTP_404_NOT_FOUND)

        try:
            cart_item = CartItem.objects.get(cart=cart, product_id=pk)
            cart_item.delete()
            return Response({'message': 'Item removed from cart successfully.'}, status=status.HTTP_200_OK)
        except CartItem.DoesNotExist:
            return Response({'error': 'Item not found in cart.'}, status=status.HTTP_404_NOT_FOUND)



class CheckoutView(generics.GenericAPIView):
    def post(self, request):
        session = request.session.session_key
        cart = session.get('cart', {})
        for product_id, item in cart.items():
            product = Product.objects.get(id=product_id)
            product.inventory_count -= item['quantity']
            if product.inventory_count == 0:
                product.is_active = False
            product.save()
        session['cart'] = {}
        session.save()
        return Response({'message': 'Purchase completed successfully.'}, status=status.HTTP_200_OK)
