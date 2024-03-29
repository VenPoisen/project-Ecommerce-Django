from django.contrib import admin
from .models import Product, Variation, ProductImage
from .forms import RequiredVariation


class VariationInline(admin.TabularInline):
    model = Variation
    formset = RequiredVariation
    min_num = 1
    extra = 0
    can_delete = True


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    min_num = 1
    extra = 1
    can_delete = True


class VariationAdmin(admin.ModelAdmin):
    list_display = ('product', 'name', 'price', 'promo_price', 'stock')
    list_filter = ('product',)
    list_editable = ('stock',)


class ProductAdmin(admin.ModelAdmin):
    inlines = [
        ProductImageInline,
        VariationInline,
    ]
    list_display = ('id', 'name', 'slug', 'summary',
                    'get_formatted_price', 'get_formatted_promo_price', 'category', 'var_type')
    list_display_links = ('id', 'name', 'slug',)


admin.site.register(Product, ProductAdmin)
admin.site.register(Variation, VariationAdmin)
