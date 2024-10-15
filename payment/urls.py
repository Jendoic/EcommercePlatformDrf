from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PaymentViewSet, PaystackWebhookView

router = DefaultRouter()
router.register(r'payments', PaymentViewSet, basename='payments')

urlpatterns = [
    path('', include(router.urls)),
    path('verify_payment',PaystackWebhookView.as_view(), name='verify_payment' )
]
