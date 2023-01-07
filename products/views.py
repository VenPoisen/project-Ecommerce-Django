from profiles.models import Address, Profile
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
        stock_variation = variation.stock
        product = variation.product

        product_id = product.id
        product_name = product.name
        variation_name = variation.name or ''
        unit_price = variation.price
        promo_unit_price = variation.promo_price
        quantity = 1
        slug = product.slug
        image = product.image

        if image:
            image = image.name
        else:
            image = ''

        if variation.stock < 1:
            messages.error(
                self.request,
                'Product Unavailable'
            )
            return redirect(http_referer)

        if not self.request.session.get('cart'):
            self.request.session['cart'] = {}
            self.request.session.save()

        cart = self.request.session['cart']

        if variation_id in cart:
            cart_quantity = cart[variation_id]['quantity']
            cart_quantity += 1

            if stock_variation < cart_quantity:
                messages.warning(
                    self.request,
                    f'Insufficient stock for {cart_quantity}x in product "{product_name}". Added {stock_variation}x in cart.'
                )
                cart_quantity = stock_variation

            cart[variation_id]['quantity'] = cart_quantity
            cart[variation_id]['quantitative_price'] = unit_price * cart_quantity
            cart[variation_id]['promo_quantitative_price'] = promo_unit_price * cart_quantity

        else:
            cart[variation_id] = {
                'product_id': product_id,
                'product_name': product_name,
                'variation_name': variation_name,
                'variation_id': variation_id,
                'unit_price': unit_price,
                'promo_unit_price': promo_unit_price,
                'quantitative_price': unit_price,
                'promo_quantitative_price': promo_unit_price,
                'quantity': 1,
                'slug': slug,
                'image': image,
            }

        self.request.session.save()

        messages.success(
            self.request,
            f'Product {product.name} {variation.name} add to cart {cart[variation_id]["quantity"]}x.'
        )

        return redirect(http_referer)


class RemoveFromCart(View):
    def get(self, *args, **kwargs):
        http_referer = self.request.META.get(
            'HTTP_REFERER',
            reverse('products:cart')
        )
        variation_id = self.request.GET.get('vid')

        if not variation_id:
            return redirect(http_referer)

        if not self.request.session.get('cart'):
            return redirect(http_referer)

        if variation_id not in self.request.session['cart']:
            return redirect(http_referer)

        cart = self.request.session['cart'][variation_id]

        messages.info(
            self.request,
            f'{cart["product_name"]} {cart["variation_name"]} removed from cart.'
        )

        del self.request.session['cart'][variation_id]
        self.request.session.save()

        return redirect(http_referer)


class Cart(View):
    def get(self, *args, **kwargs):
        context = {
            'cart': self.request.session.get('cart', {})
        }

        return render(self.request, 'products/cart.html', context)


class Checkout(View):
    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            messages.info(
                self.request,
                'Login or create an account to proceed with the order'
            )
            return redirect('profiles:create')

        if not self.request.session['cart']:
            return redirect('products:cart')

        self.profile = Profile.objects.filter(
            user=self.request.user).first()
        self.address = Address.objects.filter(
            user=self.profile).all()

        if not self.profile or not self.address:
            messages.error(
                self.request, 'Complete your profile and address before proceeding with your order')
            return redirect('profiles:create')

        instance_address = []
        for i in range(0, self.address.count()):
            instance_address.append(self.address[i])
        first_address = instance_address[0]

        context = {
            'user': self.request.user,
            'cart': self.request.session['cart'],
            'first_address': first_address,
        }

        return render(self.request, 'products/checkout.html', context)
