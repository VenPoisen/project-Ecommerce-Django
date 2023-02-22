from django.db import models
from PIL import Image
from django.conf import settings
from django.utils.text import slugify
from utils import utils
from django.core.validators import MinValueValidator
import os


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name='name')
    summary = models.TextField(max_length=255)
    description = models.TextField()
    slug = models.SlugField(unique=True, blank=True, null=True)
    mrkt_price = models.FloatField(verbose_name='marketing price')
    promo_mrkt_price = models.FloatField(
        default=0,
        verbose_name='promotional marketing price'
    )
    category = models.CharField(
        default='T',
        max_length=1,
        choices=(
            ('T', 'Technology'),
            ('C', 'Clothes'),
            ('F', 'Furniture'),
        ))
    var_type = models.CharField(
        default='V',
        max_length=1,
        choices=(
            ('V', 'Variable'),
            ('S', 'Simple'),
        )
    )

    def get_formatted_price(self):
        return utils.price_format(self.mrkt_price)
    get_formatted_price.short_description = 'Marketing Price'

    def get_formatted_promo_price(self):
        return utils.price_format(self.promo_mrkt_price)
    get_formatted_promo_price.short_description = 'Promotional Price'

    def __str__(self):
        return self.slug

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = f'{slugify(self.name)}'
            self.slug = slug
        super().save(*args, **kwargs)


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to=r'product_img/%Y/%m/%d',
        blank=True,
        null=True, unique=True
    )

    def save(self, *args, **kwargs):
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
    name = models.CharField(max_length=50, blank=True,
                            null=True, verbose_name='Variation name')
    price = models.FloatField()
    promo_price = models.FloatField(default=0)
    stock = models.PositiveIntegerField(validators=[MinValueValidator(1)])

    def __str__(self):
        return self.name or self.product.name
