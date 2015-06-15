from django.contrib import admin
from task.models import TaskDirectory, FarmingTaskDirectory, CraftingTaskDirectory, HarvestingTaskDirectory, BuildingTaskDirectory, Task, Assignment

admin.site.register(TaskDirectory)
admin.site.register(FarmingTaskDirectory)
admin.site.register(HarvestingTaskDirectory)
admin.site.register(CraftingTaskDirectory)
admin.site.register(BuildingTaskDirectory)
admin.site.register(Task)
admin.site.register(Assignment)