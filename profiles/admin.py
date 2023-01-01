from django.contrib import admin
from . import models


class AddressInline(admin.TabularInline):
    model = models.Address
    extra = 0


class ProfileAdmin(admin.ModelAdmin):
    inlines = [
        AddressInline
    ]
    list_display = ('user', 'cpf', )


class AddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'address', 'city',
                    'state',)


admin.site.register(models.Profile, ProfileAdmin)
admin.site.register(models.Address, AddressAdmin)
