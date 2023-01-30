from django.contrib import admin
from . import models


class ItemDemandInline(admin.TabularInline):
    model = models.ItemDemand
    extra = 1


class AddressDemandInline(admin.TabularInline):
    model = models.AddressDemand
    extra = 0

    readonly_fields = ("address_id",)


class DemandAdmin(admin.ModelAdmin):
    inlines = [
        ItemDemandInline,
        AddressDemandInline
    ]


admin.site.register(models.Demand, DemandAdmin)
admin.site.register(models.ItemDemand)
admin.site.register(models.AddressDemand)
