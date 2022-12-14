from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.conf import settings
import os


class Demand(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total = models.FloatField()
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
