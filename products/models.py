from django.db import models
from PIL import Image
from django.conf import settings
from django.utils.text import slugify
import os


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name='name')
    summary = models.TextField(max_length=255)
    description = models.TextField()
    image = models.ImageField(
        upload_to=r'product_img/%Y/%m/%d',
        blank=True,
        null=True
    )
    slug = models.SlugField(unique=True, blank=True, null=True)
    mrkt_price = models.FloatField(verbose_name='marketing price')
    promo_mrkt_price = models.FloatField(
        default=0,
        verbose_name='promotional marketing price'
    )
    var_type = models.CharField(
        default='V',
        max_length=1,
        choices=(
            ('V', 'Variable'),
            ('S', 'Simple'),
        )
    )

    def __str__(self):
        return self.slug

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = f'{slugify(self.name)}'
            self.slug = slug
        super().save(*args, **kwargs)

        if self.image:
            self.resize_image(self.image.name, 800)

    @staticmethod
    def resize_image(img_name, new_width):
        img_path = os.path.join(settings.MEDIA_ROOT, img_name)
        img = Image.open(img_path)
        width, height = img.size
        new_height = round((new_width * height) / width)

        if width <= new_width:
            img.close()
            return

        new_img = img.resize((new_width, new_height), Image.LANCZOS)
        new_img.save(
            img_path,
            optimize=True,
            quality=60,
        )
        new_img.close()


class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, blank=True, null=True)
    price = models.FloatField()
    promo_price = models.FloatField(default=0)
    stock = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.name or self.product.name
