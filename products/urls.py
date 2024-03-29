from django.urls import path
from . import views


app_name = 'products'

urlpatterns = [
    path('', views.ProductList.as_view(), name='list'),
    path('search/', views.Search.as_view(), name='search'),
    path('cart/', views.Cart.as_view(), name='cart'),
    path('addtocart/', views.AddToCart.as_view(), name='addcart'),
    path('removefromcart/', views.RemoveFromCart.as_view(), name='removecart'),
    path('cart/getcep/', views.get_cart_cep_price, name='cep_cart_price'),
    path('checkout/', views.Checkout.as_view(), name='checkout'),
    path('checkout/getaddress/', views.get_checkoutaddress, name='getaddress'),
    path('category/<str:category>',
         views.ProductCategory.as_view(), name='category'),
    path('<slug>', views.ProductDetails.as_view(), name='detail'),

]
