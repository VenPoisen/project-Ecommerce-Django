from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.conf import settings
from datetime import date
import os


class Demand(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total = models.FloatField()
    shipping_price = models.FloatField()
    total_w_shipping = models.FloatField()
    total_qty = models.PositiveIntegerField()
    creation_date = models.DateField(default=date.today)
    status = models.CharField(
        default='C',
        max_length=1,
        choices=(
            ('A', 'Approved'),
            ('C', 'Created'),
            ('D', 'Disapproved'),
            ('P', 'Pending'),
            ('S', 'Sent'),
            ('F', 'Finished'),
        ),
    )

    def __str__(self) -> str:
        return f'Order N. {self.pk}'


class ItemDemand(models.Model):
    order = models.ForeignKey(Demand, on_delete=models.CASCADE)
    product = models.CharField(max_length=255)
    product_id = models.PositiveIntegerField()
    variation = models.CharField(max_length=255)
    variation_id = models.PositiveIntegerField()
    price = models.FloatField()
    promo_price = models.FloatField(default=0)
    quantity = models.PositiveIntegerField()
    image = models.CharField(max_length=2000)

    def __str__(self) -> str:
        return f'Item from {self.order}'

    class Meta:
        verbose_name = 'Order Item'
        verbose_name_plural = 'Order Items'


class AddressDemand(models.Model):
    order = models.ForeignKey(Demand, on_delete=models.CASCADE)
    address_id = models.PositiveIntegerField()
    address = models.CharField(max_length=50)
    number = models.CharField(max_length=8, blank=True, null=True)
    complement = models.CharField(max_length=30, blank=True, null=True)
    city = models.CharField(max_length=30)
    cep = models.CharField(max_length=8)

    def __str__(self):
        return self.address

    class Meta:
        verbose_name = 'Address'
        verbose_name_plural = 'Addresses'
