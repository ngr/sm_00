from django.test import TestCase
from django.utils import timezone
from django.core.urlresolvers import reverse
import datetime
from random import random

from slave.models import Slave, SlaveManager, RaceDefaults
from skill.models import Skill, SkillTrained
from task.farming import Plant

from slave.settings import *

def push_base_skill():
    cursor = connection.cursor()
    cursor.execute("""INSERT INTO  `dj_sm_00`.`skill_skill`
     ( `id` , `name` , `primary_attribute` , `difficulty` )
    VALUES ( NULL ,  'Learning1',  '0',  '1' );""")
    print("Executed raw SQL to create learning skill")
    return

def get_current_db_skills():
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM `dj_sm_00`.`skill_skill` WHERE 1;")
    for row in cursor.fetchone():
        print("Row:", row)
    return row


def create_skill(name='Test skill', pr_attr=0, difficulty=1):
    """ Creates a skill """
    s = Skill(name=name, primary_attribute=pr_attr, difficulty=difficulty)
    s.save()
    return s


def create_slave(name='Slave', age=1):
    """ Creates a Slave with dayas_delta age """
    birth_time = timezone.now() - datetime.timedelta(seconds=(GAME_YEAR * age))
    sl = Slave.objects.spawn(name=name, date_birth=birth_time)
#    sl = Slave.objects.spawn()
#    print("create_slave() created slave", sl)
    return sl

def train_skill(sl=1, sk=1, level=50):
    """ Makes skilltrained record """
    st = SkillTrained.objects.set_st(sl, sk, level)
    return st

def make_plant(sk=None):
    if not sk:
        sk = create_skill()
    p = Plant(name='Test Corn', primary_skill=sk)
    p.save()
    
    p.secondary_skill.add(create_skill())
    p.secondary_skill.add(create_skill())

    return p

