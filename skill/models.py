from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
#from django.core.exceptions import ObjectDoesNotExist
from django.db.models.base import ObjectDoesNotExist
from slave.models import Slave
from slave.settings import *

class Skill(models.Model):
    """ This is the main list of skills """

    name = models.CharField(max_length=127)
    primary_attribute =  models.PositiveSmallIntegerField(choices=ATTRIBUTE_CHOICES)
    difficulty = models.PositiveSmallIntegerField(default=1)
    required_skills = models.ManyToManyField("self", symmetrical=False, null=True)
   
    def __str__(self):
        return self.name

class STManager(models.Manager):
    """" ST - stands for Skill Trained. This is a custom model manager. """
    def set_st(self, slave, skill, level=0):
        """ This method assignes the 'skill' to 'slave' at 'level'
            There are certain checks performed here. If you change test well! """

        print("Setting to slave skill at level:", slave, skill, level)

        st = SkillTrained.objects.filter(slave=slave, skill=skill)
        if st:
            print("ST record exists. Should try to update.", st)
            if self.skill_available(slave, skill):
                print("Skill available. Updating to level:", level)
                st.update(level=level)
            else:
                print("Skill is not available.")
        else:
            print("No ST record. Creating new one...", st)
            if self.skill_available(slave, skill):
                print("skill_available() returned True")
                st = SkillTrained(slave=slave, skill=skill, level=level)
                st.save()
            else:
                print("Skill is not available")

    def inc_st(self, slave, skill):
        """ This is a shortcut to increase skill by 1 """
        st = SkillTrained.objects.filter(slave=slave, skill=skill)
        self.set_st(slave, skill, st[0].level + 1)


    def skill_available(self, slave, skill):
        """ This helper checks if given skill should be available to the slave """
    # The following exception is required for base skills with no parents
        req = skill.required_skills
        if req:
            return True # This happens with "base" skills.
        
        print("Slave has required skill at level:",\
                SkillTrained.objects.filter(slave=slave, skill=req.get()).get().level)

        return True if SkillTrained.objects.filter(slave=slave, skill=req.get()).get().level\
                >= SKILL_LEVEL_REQUIREMENT else False


class SkillTrained(models.Model):
    slave = models.ForeignKey('slave.Slave')
    skill = models.ForeignKey('Skill')
    level = models.PositiveSmallIntegerField(default=1,\
            validators=[MinValueValidator(0), MaxValueValidator(100)])
    
    objects = STManager()

    def __str__(self):
        return " ".join([str(self.slave), str(self.skill), str(self.level)])

    class Meta:
        unique_together = (('slave', 'skill'))




# Create your models here.
