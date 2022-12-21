from django.urls import path
from . import views


app_name = 'products'

urlpatterns = [
    path('', views.ProductList.as_view(), name='list'),
    path('<slug>', views.ProductDetails.as_view(), name='detail'),
    path('addtocart/', views.AddToCart.as_view(), name='addcart'),
    path('removefromcart/', views.RemoveFromCart.as_view(), name='removecart'),
    path('cart/', views.Cart.as_view(), name='cart'),
    path('finish/', views.Finish.as_view(), name='finish'),
]
