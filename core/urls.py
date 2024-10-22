from django.contrib import admin
from django.urls import path, include
from payment.views import PaystackWebhookView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('auths.urls')),
    path('api/v1/', include('categories.urls')),
    path('api/v1/', include('store.urls')),
    path('api/v1/', include('carts.urls')),
    path('api/v1/', include('orders.urls')),
    path('api/v1/', include('payment.urls')),
    path('api/v1/verify_payment',PaystackWebhookView.as_view(), name='verify_payment' )
    
   
]