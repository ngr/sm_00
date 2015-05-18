from django.contrib import admin
from item.models import ItemBaseParam, ItemParamDirectory, ItemDirectory, ItemRecipe, Item

admin.site.register(ItemBaseParam)
admin.site.register(ItemParamDirectory)
admin.site.register(ItemDirectory)
admin.site.register(ItemRecipe)
admin.site.register(Item)
