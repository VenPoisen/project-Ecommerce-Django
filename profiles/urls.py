from django.urls import path
from . import views


app_name = 'profiles'

urlpatterns = [
    path('', views.Create.as_view(), name='create'),
    path('address/', views.AddressList.as_view(), name='address'),
    path('address/<int:pk>',
         views.AddressUpdate.as_view(), name='addressdetails'),
    path('address-create/',
         views.AddressCreate.as_view(), name='addresscreate'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path(
        'address/address/', views.cep_update, name='cepupdate'
    ),
]
