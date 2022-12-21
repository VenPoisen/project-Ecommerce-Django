from django.shortcuts import render
from django.views.generic.list import ListView
from django.views import View
from django.http import HttpResponse
from . import models


class ProductList(ListView):
    model = models.Product
    template_name = 'products/list.html'
    context_object_name = 'products'
    paginate_by = 6


class ProductDetails(View):
    pass


class AddToCart(View):
    pass


class RemoveFromCart(View):
    pass


class Cart(View):
    pass


class Finish(View):
    pass
