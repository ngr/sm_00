from django.contrib import admin
from task.models import Task, Farming
from task.farming import Plant

admin.site.register(Plant)
admin.site.register(Farming)
admin.site.register(Task)


# Register your models here.
