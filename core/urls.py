from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('auths.urls')),
    path('api/v1/', include('categories.urls')),
    path('api/v1/', include('store.urls')),
    path('api/v1/', include('carts.urls')),
    path('api/v1/', include('orders.urls')),
    path('api/v1/', include('payment.urls')),
    
   
]