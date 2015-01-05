from django.db import models
from django.db.models import Q
from django.core.validators import MaxValueValidator, MinValueValidator
#from django.core.exceptions import ObjectDoesNotExist
from django.db.models.base import ObjectDoesNotExist

from random import random, randrange

#from slave.models import Slave
from slave.settings import *
from slave.helpers import *

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
    def set_st(self, slave, skill, exp=0):
        """ This method assignes the 'skill' to 'slave' with 'exp'
            There are certain checks performed here. If you change test well! """

        print("Setting to slave skill with exp:", slave, skill, exp)

        exp = fit_to_range_int(exp, 0)
        print("Fitted exp:", exp)
#        level, level1 = level1, level

        st = SkillTrained.objects.filter(slave=slave, skill=skill)
        if st:
            print("ST record exists. Should try to update.", st)
            if self.__skill_available(slave, skill):
                print("Skill available. Updating exp:", exp)
                st.update(exp=exp)
            else:
                print("Skill is not available.")
        else:
            print("No ST record. Creating new one...", st)
            if self.__skill_available(slave, skill):
                print("skill_available() returned True")
                st = SkillTrained(slave=slave, skill=skill, exp=exp)
                st.save()
            else:
                print("Skill is not available")

    def add_exp(self, slave, skill, exp=1):
        """ This is a shortcut to increase skill experience """
        st = SkillTrained.objects.filter(slave=slave, skill=skill)
        if not st:
            st = SkillTrained(slave=slave, skill=skill, exp=exp)
            st.save()
        else:
            self.set_st(slave, skill, st[0].exp + exp)


    def get_available_skills(self, slave):
        """ Return a list of skills with level currently available to train/use """
    # This looks quite comlicated... 
    # The idea is to check if required skills are trained enough to open the new skill
        r = Skill.objects.filter(Q(required_skills__in=Skill.objects.filter(skilltrained__slave=slave,skilltrained__exp__gte=MIN_EXP_FOR_CHILD_SKILLS))|Q(required_skills__isnull=True)).order_by('difficulty').order_by('required_skills', 'difficulty')
    # Now we check if there are available skills with zero exp. We set it to 1 to make skill really available
        refresh = False
        for s in r:
            if self.get_skill_level(slave, s) == 0:
                print("New skill available!", s)
                self.add_exp(slave, s)
                refresh = True
    # SkillTrained objects have been updated need to refresh result!
        if refresh:
            r = Skill.objects.filter(Q(required_skills__in=Skill.objects.filter(skilltrained__slave=slave,skilltrained__exp__gte=MIN_EXP_FOR_CHILD_SKILLS))|Q(required_skills__isnull=True)).order_by('difficulty').order_by('required_skills', 'difficulty')
        return r


    def get_slave_skills(self, slave):
        """ Brand new function to return skills with exp """
        return SkillTrained.objects.filter(skill__in=Skill.objects.filter(Q(required_skills__in=Skill.objects.filter(skilltrained__slave=slave,skilltrained__exp__gte=MIN_EXP_FOR_CHILD_SKILLS))|Q(required_skills__isnull=True)).order_by('difficulty').order_by('required_skills', 'difficulty'), slave=slave)




    def get_skill_level(self, slave, skill):
        """ Returns the current skill level of slave """
        st = SkillTrained.objects.filter(slave=slave, skill=skill)
        return exp_to_lev(st.get().exp) if st else 0
    
    def use_skill(self, slave, skill, bonus=0):
        """ Returns boolean result of using skill. Bonus in range -1:1 can modify result """
        skl = self.get_skill_level(slave, skill)
        if not (-1.0 <= bonus <= 1.0):
            raise AttributeError("Bonus invalid.")

        skl = 0.99 if (skl/100.0 + bonus) >= 1 else skl/100.0 + bonus
        skl = 0 if skl < 0 else skl
        print("Skill level with bonus:", skl)

        return random() < skl

    def __skill_available(self, slave, skill):
        """ This helper checks if given skill should be available to the slave """
    # The following exception is required for base skills with no parents
        req = skill.required_skills
        if req:
            return True # This happens with "base" skills.

        print("Slave has required skill with exp:",\
                SkillTrained.objects.filter(slave=slave, skill=req.get()).get().exp)

        return True if exp_to_lev(SkillTrained.objects.filter(slave=slave, skill=req.get()).get().exp)\
                >= SKILL_LEVEL_REQUIREMENT else False



class SkillTrained(models.Model):
    slave = models.ForeignKey('slave.Slave')
    skill = models.ForeignKey('Skill')
#    level = models.PositiveSmallIntegerField(default=1,\
#            validators=[MinValueValidator(0), MaxValueValidator(100)])
    exp   = models.PositiveIntegerField(default=1,\
            validators=[MinValueValidator(0)])

    
    objects = STManager()

    def __str__(self):
        return " ".join([str(self.slave), str(self.skill), str(exp_to_lev(self.exp))])

    class Meta:
        unique_together = (('slave', 'skill'))

################
#
###############

    def get_skill_exp(self):
        return self.exp



# Create your models here.
