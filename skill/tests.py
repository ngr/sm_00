from django.test import TestCase
from django.utils import timezone
from django.db import connection

#from django.core.urlresolvers import reverse
import datetime
from random import random, randrange

from skill.models import Skill, SkillTrained
from slave.models import Slave, SlaveManager, RaceDefaults
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
#    push_base_skill()
#    print(get_current_db_skills())
#    print("Skill obj all() get():", Skill.objects.all().get())
    s = Skill(name=name, primary_attribute=pr_attr, difficulty=difficulty)
    s.save()
#    print(get_current_db_skills())
#    s.required_skill.add(bs)
#    print(s)
    return s


def create_slave(name='Slave', age=1):
    """ Creates a Slave with dayas_delta age """
    birth_time = timezone.now() - datetime.timedelta(seconds=(GAME_YEAR * age))
    sl = Slave.objects.spawn(name=name, date_birth=birth_time)
#    sl = Slave.objects.spawn()
#    print("create_slave() created slave", sl)
    return sl


class SkillManagerTests(TestCase):
    """ Tests for SkillTrained models. It represents the level
    of skill trained for each Slave. """

    def test_set_st_available_skill(self):
        sl = create_slave()
        print("Created test slave", sl)
        sk1 = create_skill()
        print("Created test skill", sk1)

        SkillTrained.objects.set_st(sl, sk1, 3)
        print("Created a connection")
        st = SkillTrained.objects.filter(slave=sl)

        self.assertEqual(SkillTrained.objects.filter(slave=sl, skill=sk1).get().level, 3)

    def test_create_st_unavailable_skill(self):
        sl = create_slave()
        print("Created test slave", sl)
        sk1 = create_skill()
        print("Created test skill", sk1)

        sk2 = create_skill()
        sk2.required_skills.add(sk1)
        # Нихера не работает. должно фейлить, а оно пускает.
        # Тесты эти автоматические с базой работают через жопу.
        SkillTrained.objects.set_st(sl, sk2, 3)







# Create your tests here.
