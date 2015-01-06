from django.contrib import admin
from item.models import ItemDirectory, FoodDirectory, MaterialDirectory, Item
#, Food, Material
#from item.models import ItemDirectory, FoodDirectory, ItemType, Item, Food


class ItemDirectoryAdmin(admin.ModelAdmin):
    list_display = ('_name', 'get_child_types', 'is_core')
#    list_filter = ['get_type']
    list_ordering = ['is_core']

admin.site.register(ItemDirectory, ItemDirectoryAdmin)
admin.site.register(FoodDirectory)
admin.site.register(MaterialDirectory)
#admin.site.register(ItemType)
admin.site.register(Item)
#admin.site.register(Food)
#admin.site.register(Material)

# Register your models here.
