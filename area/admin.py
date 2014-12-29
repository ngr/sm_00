from django.contrib import admin
#from area.models import Region, Location, FarmingField, HousingDistrict, Warehouse, FoodStock
from area.models import Region, Location, FarmingField, HousingDistrict, WarehouseBuilding, Warehouse, FoodStock

admin.site.register(Region)
admin.site.register(Location)
admin.site.register(FarmingField)
admin.site.register(HousingDistrict)
admin.site.register(WarehouseBuilding)
admin.site.register(Warehouse)
admin.site.register(FoodStock)

# Register your models here.
