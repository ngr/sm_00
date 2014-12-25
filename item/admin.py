from django.contrib import admin
from item.models import ItemDirectory, FoodDirectory, MaterialDirectory, Item, Food, Material
#from item.models import ItemDirectory, FoodDirectory, ItemType, Item, Food


admin.site.register(ItemDirectory)
admin.site.register(FoodDirectory)
admin.site.register(MaterialDirectory)
#admin.site.register(ItemType)
admin.site.register(Item)
admin.site.register(Food)
admin.site.register(Material)

# Register your models here.
