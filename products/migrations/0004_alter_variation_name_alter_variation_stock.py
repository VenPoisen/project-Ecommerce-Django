# Generated by Django 4.1.4 on 2023-01-07 16:09

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_alter_product_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='variation',
            name='name',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Variation name'),
        ),
        migrations.AlterField(
            model_name='variation',
            name='stock',
            field=models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)]),
        ),
    ]
