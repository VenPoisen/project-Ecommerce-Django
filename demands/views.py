from django.shortcuts import render, redirect, reverse
from django.views.generic import ListView, DetailView
from django.views import View
from django.http import HttpResponse
from django.contrib import messages
from products.models import Variation
from utils import utils
from .models import ItemDemand, Demand


class DispatchLoginRequired(View):
    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('profiles:create')

        return super().dispatch(*args, **kwargs)

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(user=self.request.user)
        return qs


class Pay(DispatchLoginRequired, DetailView):
    template_name = 'orders/pay.html'
    model = Demand
    pk_url_kwarg = 'pk'
    context_object_name = 'order'


class SaveOrder(View):
    template_name = 'orders/pay.html'
    # TODO: adicionar calculo de frete

    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            messages.error(
                self.request, 'You need to register or login.')
            return redirect('profiles:create')

        if not self.request.session.get('cart'):
            messages.error(
                self.request, 'Your cart is empty.')
            return redirect('products:list')

        cart = self.request.session.get('cart')
        cart_var_ids = [v for v in cart]
        bd_variations = list(
            Variation.objects.select_related(
                'product').filter(id__in=cart_var_ids)
        )

        for variation in bd_variations:
            vid = str(variation.id)

            stock = variation.stock
            cart_qty = cart[vid]['quantity']
            unit_price = cart[vid]['unit_price']
            promo_unit_price = cart[vid]['promo_unit_price']

            error_msg_stock = ''

            if stock < cart_qty:
                cart[vid]['quantity'] = stock
                cart[vid]['quantitative_price'] = stock * unit_price
                cart[vid]['promo_quantitative_price'] = stock * promo_unit_price

                error_msg_stock = 'Insufficient stock for some products in your cart. '\
                    'We have reduced the quantity of these products. Please check which products were affected below.'

            if error_msg_stock:
                messages.error(
                    self.request,
                    error_msg_stock
                )

                self.request.session.save()
                return redirect('products:cart')

        qty_total_cart = utils.cart_total_qty(cart)
        value_total_cart = utils.cart_totals(cart)

        order = Demand(
            user=self.request.user,
            total=value_total_cart,
            total_qty=qty_total_cart,
            status='C',
        )
        order.save()

        ItemDemand.objects.bulk_create(
            [
                ItemDemand(
                    order=order,
                    product=v['product_name'],
                    product_id=v['product_id'],
                    variation=v['variation_name'],
                    variation_id=v['variation_id'],
                    price=v['quantitative_price'],
                    promo_price=v['promo_quantitative_price'],
                    quantity=v['quantity'],
                    image=v['image'],
                ) for v in cart.values()
            ]
        )

        del self.request.session['cart']
        return redirect(
            reverse(
                'orders:pay',
                kwargs={
                    'pk': order.pk
                }
            )
        )


class OrderList(DispatchLoginRequired, ListView):
    model = Demand
    context_object_name = 'orders'
    template_name = 'orders/orderlist.html'
    paginate_by = 10
    ordering = ['-id']


class OrderDetails(DispatchLoginRequired, DetailView):
    model = Demand
    context_object_name = 'order'
    template_name = 'orders/orderdetails.html'
    pk_url_kwarg = 'pk'
