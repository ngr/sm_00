from django.contrib import admin
from item.models import ItemDirectory, ItemType, Item, Food
#from item.models import ItemDirectory, FoodDirectory, ItemType, Item, Food


admin.site.register(ItemDirectory)
#admin.site.register(FoodDirectory)
admin.site.register(ItemType)
admin.site.register(Item)
admin.site.register(Food)

# Register your models here.
