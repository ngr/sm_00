from django.contrib import admin
from item.models import ItemParam, ItemBaseParam, ItemParamDirectory, ItemDirectory, ItemRecipe, Item

#class ItemDirectoryAdmin(admin.ModelAdmin):
#    list_display = ('name', 'get_child_types', 'is_core')
#    list_filter = ['get_type']
#    list_ordering = ['is_core']

admin.site.register(ItemParam)
admin.site.register(ItemBaseParam)
admin.site.register(ItemParamDirectory)
admin.site.register(ItemDirectory)
admin.site.register(ItemRecipe)
admin.site.register(Item)
