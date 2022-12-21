from django.contrib import admin
from .models import Product, Variation


class VariationInline(admin.TabularInline):
    model = Variation
    extra = 1


class VariationAdmin(admin.ModelAdmin):
    list_display = ('product', 'name', 'price', 'promo_price', 'stock')
    list_filter = ('product',)


class ProductAdmin(admin.ModelAdmin):
    inlines = [
        VariationInline
    ]
    list_display = ('id', 'name', 'slug', 'summary',
                    'get_formatted_price', 'get_formatted_promo_price', 'var_type')
    list_display_links = ('id', 'name', 'slug',)


admin.site.register(Product, ProductAdmin)
admin.site.register(Variation, VariationAdmin)
