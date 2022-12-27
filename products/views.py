from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views import View
from django.http import HttpResponse
from . import models


class ProductList(ListView):
    model = models.Product
    template_name = 'products/list.html'
    context_object_name = 'products'
    paginate_by = 6


class ProductDetails(DetailView):
    model = models.Product
    template_name = 'products/detail.html'
    context_object_name = 'product'
    slug_url_kwarg = 'slug'


class AddToCart(View):
    pass


class RemoveFromCart(View):
    pass


class Cart(View):
    pass


class Finish(View):
    pass
