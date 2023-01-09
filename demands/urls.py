from django.urls import path
from . import views


app_name = 'orders'

urlpatterns = [
    path('pay/<int:pk>', views.Pay.as_view(), name='pay'),
    path('saveorder/', views.SaveOrder.as_view(), name='saveorder'),
    path('orderdetails/', views.OrderDetails.as_view(), name='orderdetails'),
]
