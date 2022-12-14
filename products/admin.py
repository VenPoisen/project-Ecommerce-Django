from django.contrib import admin
from .models import Product, Variation


class VariationInline(admin.TabularInline):
    model = Variation
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    inlines = [
        VariationInline
    ]
    list_display = ('id', 'name', 'slug', 'summary',
                    'mrkt_price', 'promo_mrkt_price', 'var_type')
    list_editable = ('mrkt_price', 'promo_mrkt_price',)
    list_display_links = ('id', 'name', 'slug',)


admin.site.register(Product, ProductAdmin)
admin.site.register(Variation)
