from django.contrib import admin
from . import models


class AddressInline(admin.TabularInline):
    model = models.Address
    extra = 1


class ProfileAdmin(admin.ModelAdmin):
    inlines = [
        AddressInline
    ]


admin.site.register(models.Profile, ProfileAdmin)
admin.site.register(models.Address)
