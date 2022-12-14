from django.contrib import admin
from . import models


class ItemDemandInline(admin.TabularInline):
    model = models.ItemDemand
    extra = 1


class DemandAdmin(admin.ModelAdmin):
    inlines = [
        ItemDemandInline
    ]


admin.site.register(models.Demand, DemandAdmin)
admin.site.register(models.ItemDemand)
