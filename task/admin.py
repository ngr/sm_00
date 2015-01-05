from django.contrib import admin
from task.models import TaskDirectory, FarmingTaskDirectory, Task, Assignment
from task.farming import Plant




admin.site.register(TaskDirectory)
admin.site.register(FarmingTaskDirectory)
admin.site.register(Task)
admin.site.register(Plant)
admin.site.register(Assignment)
# Register your models here.
