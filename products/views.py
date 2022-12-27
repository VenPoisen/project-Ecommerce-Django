from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.urls import reverse
from django.views import View
from django.http import HttpResponse
from django.contrib import messages
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
    def get(self, *args, **kwargs):
        http_referer = self.request.META.get(
            'HTTP_REFERER',
            reverse('products:list')
        )
        variation_id = self.request.GET.get('vid')

        if not variation_id:
            messages.error(
                self.request,
                'Product does not exist'
            )
            return redirect(http_referer)

        variation = get_object_or_404(models.Variation, id=variation_id)

        if not self.request.session.get('cart'):
            self.request.session['cart'] = {}
            self.request.session.save()

        cart = self.request.session['cart']

        if variation_id in cart:
            # TODO: Variation exists on cart
            pass

        else:
            # TODO: Variation does not exist on cart
            pass

        return HttpResponse(f'{variation.product} {variation.name}')


class RemoveFromCart(View):
    pass


class Cart(View):
    pass


class Finish(View):
    pass
