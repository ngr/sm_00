from django.contrib import admin
#from area.models import Region, Location, FarmingField, HousingDistrict, Warehouse, FoodStock
from area.models import Region, Location, FarmingField, HousingDistrict, BuildingType, BuildingMaterialRecipe, Workshop, Warehouse

admin.site.register(Region)
admin.site.register(Location)
admin.site.register(FarmingField)
admin.site.register(HousingDistrict)
admin.site.register(BuildingType)
admin.site.register(BuildingMaterialRecipe)
admin.site.register(Workshop)
admin.site.register(Warehouse)

# Register your models here.
