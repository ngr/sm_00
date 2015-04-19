from django.contrib import admin
from area.models import Region, Location, LocationType, LocationDirectory

admin.site.register(Region)
admin.site.register(Location)
admin.site.register(LocationType)
admin.site.register(LocationDirectory)


# Register your models here.
