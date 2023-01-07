from django.urls import path
from . import views


app_name = 'orders'

urlpatterns = [
    path('', views.Pay.as_view(), name='pay'),
    path('closeorder/', views.CloseOrder.as_view(), name='closeorder'),
    path('orderdetails/', views.OrderDetails.as_view(), name='orderdetails'),
]
