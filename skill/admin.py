from django.contrib import admin
#from slave.models import Slave, RaceDefaults
from skill.models import Skill, SkillTrained


admin.site.register(Skill)
admin.site.register(SkillTrained)

# Register your models here.
