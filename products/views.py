from utils.utils import price_format, cart_totals
from utils import shippingcalculator
from utils import addressgenerator
from django.http import JsonResponse
from profiles.models import Address, Profile
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.urls import reverse
from django.views import View
from django.contrib import messages
from django.db.models import Q
from . import models
from profiles.forms import CEPForm


class ProductList(ListView):
    model = models.Product
    template_name = 'products/list.html'
    context_object_name = 'products'
    paginate_by = 6
    ordering = ['-id']


class Search(ProductList):
    def get_queryset(self, *args, **kwargs):
        self.term = self.request.GET.get('term')
        qs = super().get_queryset(*args, **kwargs)

        if not self.term:
            return qs

        qs = qs.filter(
            Q(name__icontains=self.term) |
            Q(summary__icontains=self.term) |
            Q(description__icontains=self.term)
        )

        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        search_term = self.term

        if not search_term:
            return ctx

        ctx.update({
            "additional_url_query": f'&term={search_term}',
        })

        return ctx


class ProductCategory(ProductList):
    def get_queryset(self, *args, **kwargs):
        category = self.kwargs.get('category', None)
        qs = super().get_queryset(*args, **kwargs)

        if not category:
            return qs

        qs = qs.filter(category__iexact=category)

        return qs


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
        variation_quantity_add = self.request.GET.get('qty')

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
        slug = product.slug
        category = product.category
        images = models.ProductImage.objects.filter(
            product_id=product_id).first()
        image = images.image

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

        error_msg_stock = f'Insufficient stock for "{product_name} {variation.name}". There is only {stock_variation} in stock.'

        if variation_id in cart:
            cart_quantity = cart[variation_id]['quantity']
            cart_quantity += int(variation_quantity_add)

            if stock_variation < cart_quantity:
                messages.warning(
                    self.request,
                    error_msg_stock
                )
                return redirect(http_referer)

            cart[variation_id]['quantity'] = cart_quantity
            cart[variation_id]['quantitative_price'] = unit_price * cart_quantity
            cart[variation_id]['promo_quantitative_price'] = promo_unit_price * cart_quantity

        else:
            if stock_variation < int(variation_quantity_add):
                messages.warning(
                    self.request,
                    error_msg_stock
                )
                return redirect(http_referer)

            cart[variation_id] = {
                'product_id': product_id,
                'product_name': product_name,
                'category': category,
                'variation_name': variation_name,
                'variation_id': variation_id,
                'unit_price': unit_price,
                'promo_unit_price': promo_unit_price,
                'quantitative_price': unit_price * int(variation_quantity_add),
                'promo_quantitative_price': promo_unit_price * int(variation_quantity_add),
                'quantity': int(variation_quantity_add),
                'slug': slug,
                'image': image,
            }

        self.request.session.save()

        messages.success(
            self.request,
            f'Added {variation_quantity_add}x "{product.name} {variation.name}" to cart.'
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

        delete_qty = self.request.GET.get('del-qty')
        cart = self.request.session['cart'][variation_id]

        cart['quantity'] -= int(delete_qty)
        cart['quantitative_price'] = cart['unit_price'] * cart['quantity']
        cart['promo_quantitative_price'] = cart['promo_unit_price'] * \
            cart['quantity']
        if cart['quantity'] < 1:
            del self.request.session['cart'][variation_id]

        messages.info(
            self.request,
            f'{delete_qty}x {cart["product_name"]} {cart["variation_name"]} removed from cart.'
        )

        self.request.session.save()

        return redirect(http_referer)


class Cart(View):
    def get(self, *args, **kwargs):
        context = {
            'cart': self.request.session.get('cart', {}),
            'address': CEPForm,
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

        if not self.profile:
            messages.error(
                self.request, 'Complete your profile and address before proceeding with your order')
            return redirect('profiles:create')
        if not self.address:
            messages.error(
                self.request, 'Create a new address before proceeding with your order')
            return redirect('profiles:address')

        instance_address = []
        for i in range(0, self.address.count()):
            instance_address.append(self.address[i])
        first_address = instance_address[0]

        context = {
            'user': self.request.user,
            'cart': self.request.session['cart'],
            'addresses': self.address,
            'first_address': first_address,
        }

        return render(self.request, 'products/checkout.html', context)


def get_checkoutaddress(request, *args, **kwargs):
    if request.user.is_authenticated:
        if request.method == 'GET':
            request.profile = Profile.objects.filter(
                user=request.user).first()
            request.address = Address.objects.filter(
                user=request.profile).all()

            address_id = request.GET['inputSelect']

            address = request.address.filter(id=address_id).first()

            shipping_price = shippingcalculator.calculator(address.cep)
            shipping_price_formatted = price_format(shipping_price)

            cart = cart_totals(request.session['cart'])
            sum_cart = shipping_price + cart
            sum_cart_formatted = price_format(sum_cart)

            shipping = {
                'address': address.address,
                'complement': address.complement,
                'city': address.city,
                'cep': address.cep,
                'number': address.number,
                'neighborhood': address.neighborhood,
                'state': address.state,
                'shipping_price_formatted': shipping_price_formatted,
                'cart_total': sum_cart_formatted,
            }

            return JsonResponse(shipping)


def get_cart_cep_price(request, *args, **kwargs):
    if request.method == 'GET':
        cep_number = request.GET['inputSelect']
        cart = cart_totals(request.session['cart'])
        cart_only = price_format(cart)

        if not cep_number:
            return JsonResponse({
                "price": "false",
                "cart_only": cart_only,
            })

        valid_cep = addressgenerator.address(cep_number)
        if not valid_cep:
            return JsonResponse({
                "price": "false",
                "cart_only": cart_only,
            })

        shipping_price = shippingcalculator.calculator(cep_number)
        shipping_price_formatted = price_format(shipping_price)
        sum_cart = shipping_price + cart
        sum_cart_formatted = price_format(sum_cart)

        shipping = {
            "shipping_price_formatted": shipping_price_formatted,

            "cart_total": sum_cart_formatted,
            "price": "true",
        }
        return JsonResponse(shipping)
