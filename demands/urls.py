from django.urls import path
from . import views


app_name = 'orders'

urlpatterns = [
    path('saveorder/', views.SaveOrder.as_view(), name='saveorder'),
    path('list/', views.OrderList.as_view(), name='list'),
    path('details/<int:pk>', views.OrderDetails.as_view(), name='details'),
]
