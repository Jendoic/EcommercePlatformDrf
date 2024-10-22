import requests
from django.conf import settings
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from core import settings

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from orders.models import Order
from carts.models import Cart, CartItem
from payment.models import Payment

from .task import order_confirmation_mail


import logging

logger = logging.getLogger(__name__)



class PaymentViewSet(viewsets.ViewSet):
    def create(self, request):
        amount = request.data.get('amount')
        order_id = request.data.get('order_id')

        if not amount or not order_id:
            return Response({"error": "Amount and order ID are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return Response({"error": "Order not found."}, status=status.HTTP_404_NOT_FOUND)


        payment_data = {
            "email": request.user.email,
            "amount": int(amount) * 100,  
            "callback_url": settings.PAYSTACK_WEBHOOK_SECRET
        }

        response = requests.post(
            "https://api.paystack.co/transaction/initialize",
            json=payment_data,
            headers={
                "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
                "Content-Type": "application/json",
            },
        )

        if response.status_code == 200:
            payment_info = response.json()
            transaction_id = payment_info['data']['reference']

  
            payment = Payment.objects.create(
                order=order,  
                amount=amount,
                currency='NGN',  
                status='pending',
                transaction_id=transaction_id 
            )
            return Response(payment_info['data'], status=status.HTTP_200_OK)

        return Response(response.json(), status=response.status_code)




class PaystackWebhookView(APIView):
    @csrf_exempt  
    def post(self, request):
       
       
        event = request.data.get('event')
        data = request.data.get('data')

        logger.info(f"Webhook received: {event}, data: {data}")
        
        if event == 'charge.success':
        
            transaction_id = data.get('reference')
            try:
                payment = Payment.objects.get(transaction_id=transaction_id)
                payment.status = 'success'  
                payment.save()
                
                order = payment.order
                order.paid = True 
                order.order_status = 'processing'
                order.save() 
                
                order_confirmation_mail.delay(order.reference)
                
                # order = Order.objects.get(reference=order.reference)
                # send_mail(
                # subject="Order Confirmation",
                # message=f"Your order {order.reference} has been successfully placed.",
                # from_email=settings.EMAIL_HOST_USER,
                # recipient_list=[order.user.email],
                # fail_silently=False,
                # )
                # print(f"Order confirmation email sent to {order.user.email}")
          
                
                cart = Cart.objects.get(user=order.user)
                cart_items = CartItem.objects.filter(cart=cart)
                cart_items.delete()
              
            except Payment.DoesNotExist as e:
                logger.error(f"Payment not found for transaction id {transaction_id}. Exception: {e}")
                return Response({"error": "Payment not found."}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                logger.error(f"An error occurred: {e}")
                return Response({"error": "An error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


        elif event == 'charge.failed':

            transaction_id = data.get('reference')
            try:
                payment = Payment.objects.get(transaction_id=transaction_id)
                payment.status = 'failed' 
                payment.save()
            except Payment.DoesNotExist as e:
                logger.error(f"Payment not found for transaction id {transaction_id}. Exception: {e}")
                return Response({"error": "Payment not found."}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                logger.error(f"An error occurred: {e}")
                return Response({"error": "An error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



        return Response({"message": "Webhook received"}, status=status.HTTP_200_OK)
