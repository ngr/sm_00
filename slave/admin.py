from django.contrib import admin
from slave.models import Slave, RaceDefaults, Parent

class RaceDefaultsAdmin(admin.ModelAdmin):
    list_display = ('race', 'param', 'value')
    list_filter = ['race']

admin.site.register(Slave)
admin.site.register(RaceDefaults, RaceDefaultsAdmin)
admin.site.register(Parent)
# Register your models here.
