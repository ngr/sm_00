from django.contrib import admin
from area.models import Region, Location, LocationType, LocationDirectory, BuildingMaterialRecipe

admin.site.register(Region)
admin.site.register(Location)
admin.site.register(LocationType)
admin.site.register(LocationDirectory)
admin.site.register(BuildingMaterialRecipe)


# Register your models here.
