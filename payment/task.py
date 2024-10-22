from celery import shared_task

from django.core.mail import send_mail
from core import settings

from orders.models import Order


@shared_task
def order_confirmation_mail(order_ref):
        order = Order.objects.get(reference=order_ref)
        send_mail(
            subject="Order Confirmation",
            message=f"Your order {order.reference} has been successfully placed.",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[order.user.email],
            fail_silently=False,
        )
        print(f"Order confirmation email sent to {order.user.email}")
