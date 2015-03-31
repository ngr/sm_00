from django.test import TestCase, override_settings
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

import datetime
from random import random

from slave.models import Slave, SlaveManager, RaceDefaults
from skill.models import Skill, SkillTrained

from slave.helpers_test import *
from slave.settings import *

class ParentsTests(TestCase):
    """ These tests follow SlaveManagerTests """
    def test_is_parent_defined(self):
        mom = Slave.objects.spawn()
        son = Slave.objects.spawn(**{'parents':mom.id})
        self.assertEqual(Slave.objects.filter(parent__child=son)[0].id, mom.id)

    def test_both_parent_defined(self):
        mom = Slave.objects.spawn()
        dad = Slave.objects.spawn()
        son = Slave.objects.spawn(**{'parents':(mom.id, dad.id)})
        parents_recodred = Slave.objects.filter(parent__child=son)
        self.assertEqual((parents_recodred[0], parents_recodred[1]), (mom, dad))
    
    def test_too_many_parents(self):
        self.assertRaises(AttributeError, lambda: Slave.objects.spawn(**{'parents':(1,2,3)}))


class SlaveManagerTests(TestCase):
    attribs = ['_strength', '_intelligence', '_agility', '_charisma']
    
    def test_is_default_race_overriden(self):
        atr = {'race': 1}
        s = Slave.objects.spawn(**atr)
        self.assertEqual(s.race, 1)


    def test_is_default_attr_overriden(self):
        """ Checks if optional attribute is overriden with
        directly defined when spawning slave """
        atr = {}
        for a in __class__.attribs:
            atr[a] = 9
        s = Slave.objects.spawn(**atr)
        for a in __class__.attribs:
            self.assertEqual(getattr(s, a), 9)

    def test_is_spawned_to_db(self):
        """ Checks if spawn() puts a new Slave in DB 
        By the way checks if non-default name can be specified """
        test_name = str(random())
        s = Slave.objects.spawn(**{'name':test_name})
        self.assertEqual(Slave.objects.all().filter(_name=test_name)[0].is_alive(), True)

    def test_kill_update_in_db(self):
        """ Checks if kill() sets the date_death to now() """
        create_slave()
        Slave.objects.kill(Slave.objects.latest('_date_birth'))
        victim = Slave.objects.latest('_date_birth')
        self.assertIsNotNone(victim._date_death)

    def test_kill_with_date_specified(self):
        create_slave()
        kill_date = timezone.now().replace(microsecond=0) - datetime.timedelta(days=3)
        print(kill_date)
        Slave.objects.kill(Slave.objects.latest('_date_birth'), kill_date)
        victim = Slave.objects.latest('_date_birth')
        self.assertEqual(victim._date_death, kill_date)


class SlaveLifeTests(TestCase):
    """ Tests for age zone methods """
    
    def setUp(self):
        pass
        
##############
    def test_is_child_with_not_yet_born(self):
        """ List of slaves should not show objects
        with date_init in the future """
        time = timezone.now() + datetime.timedelta(hours=1)
        future_slave = Slave.objects.spawn(_date_birth=time)
        self.assertEqual(future_slave.is_baby(), False)

    def test_is_child_with_not_yet_born(self):
        """ List of slaves should not show objects
        with date_init in the future """
        time = timezone.now() + datetime.timedelta(hours=1)
        future_slave = Slave(_date_birth=time)
        self.assertEqual(future_slave.is_child(), False)

    def test_is_child_with_not_yet_born(self):
        """ List of slaves should not show objects
        with date_init in the future """
        time = timezone.now() + datetime.timedelta(hours=1)
        future_slave = Slave(_date_birth=time)
        self.assertEqual(future_slave.is_reproductive(), False)

    def test_is_adult_with_not_yet_born(self):
        """ List of slaves should not show objects
        with date_init in the future """
        time = timezone.now() + datetime.timedelta(hours=1)
        future_slave = Slave(_date_birth=time)
        self.assertEqual(future_slave.is_adult(), False)

#################
    def test_is_baby_with_old_slave(self):
        time = timezone.now() - \
            datetime.timedelta(seconds=(GAME_YEAR * (REPRODUCTIVE_AGE) + 1))
        test_slave = Slave(_date_birth=time)
        self.assertEqual(test_slave.is_baby(), False)

    def test_is_child_with_old_slave(self):
        time = timezone.now() - \
            datetime.timedelta(seconds=(GAME_YEAR * (REPRODUCTIVE_AGE) + 1))
        test_slave = Slave(_date_birth=time)
        self.assertEqual(test_slave.is_child(), False)

    def test_is_reproductive_with_old_slave(self):
        time = timezone.now() - \
            datetime.timedelta(seconds=(GAME_YEAR * (REPRODUCTIVE_AGE) + 1))
        test_slave = Slave(_date_birth=time)
        self.assertEqual(test_slave.is_reproductive(), False)

    def test_is_adult_with_old_slave(self):
        time = timezone.now() - \
            datetime.timedelta(seconds=(GAME_YEAR * (REPRODUCTIVE_AGE) + 1))
        test_slave = Slave(_date_birth=time)
        self.assertEqual(test_slave.is_adult(), True)

##################
    def test_is_baby_with_baby_slave(self):
        time = timezone.now() - datetime.timedelta(hours=1)
        test_slave = Slave(_date_birth=time)
        self.assertEqual(test_slave.is_baby(), True)

    def test_is_child_with_baby_slave(self):
        time = timezone.now() - \
            datetime.timedelta(seconds=(GAME_YEAR * (BABY_AGE) - 1))
        test_slave = Slave(_date_birth=time)
        self.assertEqual(test_slave.is_child(), False)

    def test_is_adult_with_baby_slave(self):
        time = timezone.now() - \
            datetime.timedelta(seconds=(GAME_YEAR * (BABY_AGE) - 1))
        test_slave = Slave(_date_birth=time)
        self.assertEqual(test_slave.is_adult(), False)

    def test_is_reproductive_with_baby_slave(self):
        time = timezone.now() - \
            datetime.timedelta(seconds=(GAME_YEAR * (BABY_AGE) - 1))
        test_slave = Slave(_date_birth=time)
        self.assertEqual(test_slave.is_reproductive(), False)

###################

    def test_is_baby_with_child_slave(self):
        time = timezone.now() - \
            datetime.timedelta(seconds=(GAME_YEAR * (CHILD_AGE - 1)))
        test_slave = Slave(_date_birth=time)
        self.assertEqual(test_slave.is_baby(), False)

    def test_is_child_with_child_slave(self):
        time = timezone.now() - \
            datetime.timedelta(seconds=(GAME_YEAR * (CHILD_AGE - 1)))
        test_slave = Slave(_date_birth=time)
        self.assertEqual(test_slave.is_child(), True)

    def test_is_reproductive_with_child_slave(self):
        time = timezone.now() - \
            datetime.timedelta(seconds=(GAME_YEAR * (CHILD_AGE - 1)))
        test_slave = Slave(_date_birth=time)
        self.assertEqual(test_slave.is_reproductive(), False)

    def test_is_adult_with_child_slave(self):
        time = timezone.now() - \
            datetime.timedelta(seconds=(GAME_YEAR * (CHILD_AGE - 1)))
        test_slave = Slave(_date_birth=time)
        self.assertEqual(test_slave.is_adult(), False)

####################
    def test_is_baby_with_reproductive_slave(self):
        time = timezone.now() - \
            datetime.timedelta(seconds=(GAME_YEAR * (REPRODUCTIVE_AGE - 1)))
        test_slave = Slave(_date_birth=time)
        self.assertEqual(test_slave.is_baby(), False)

    def test_is_child_with_reproductive_slave(self):
        time = timezone.now() - \
            datetime.timedelta(seconds=(GAME_YEAR * (REPRODUCTIVE_AGE - 1)))
        test_slave = Slave(_date_birth=time)
        self.assertEqual(test_slave.is_child(), False)

    def test_is_reproductive_with_reproductive_slave(self):
        time = timezone.now() - \
            datetime.timedelta(seconds=(GAME_YEAR * (REPRODUCTIVE_AGE - 1)))
        test_slave = Slave(_date_birth=time)
        self.assertEqual(test_slave.is_reproductive(), True)

    def test_is_adult_with_reproductive_slave(self):
        time = timezone.now() - \
            datetime.timedelta(seconds=(GAME_YEAR * (REPRODUCTIVE_AGE - 1)))
        test_slave = Slave(_date_birth=time)
        self.assertEqual(test_slave.is_adult(), True)

##################
    def test_is_alive_with_not_yet_born(self):
        time = timezone.now() + datetime.timedelta(hours=1)
        future_slave = Slave(_date_birth=time)
        self.assertEqual(future_slave.is_alive(), False)

    def test_is_alive_with_already_dead(self):
        time = timezone.now()
        birth_time = timezone.now() - datetime.timedelta(days=21)
        future_slave = Slave(_date_birth=birth_time, _date_death=time)
        self.assertEqual(future_slave.is_alive(), False)






class SlaveSkillTests(TestCase):
    """ Tests for skills.
        As far as direct access to Skill class is not recommended
        this should be done via Slave objects """

    def test_get_skill(self):
        """ Request one with one trained """
        sl = create_slave()
        sk1 = create_skill()
        SkillTrained.objects.set_st(sl, sk1, 6)
        self.assertEqual(sl.get_skill(sk1), 3)

    def test_get_skill_with_zero_st(self):
        """ Request one with none trained """
        sl = create_slave()
        sk1 = create_skill()
        self.assertEqual(sl.get_skill(sk1), 0)



class RaceDefaultsTests(TestCase):
    def test_is_attribute_in_range(self):
        attribs = ['strength', 'intelligence', 'agility', 'charisma']
        for a in attribs:
            for param in RaceDefaults.objects.all().filter(param=a):
                self.assertIn(param.value, range(1,11))

"""
def push_base_skill():
    cursor = connection.cursor()
    cursor.execute(""INSERT INTO  `dj_sm_00`.`skill_skill`
     ( `id` , `name` , `primary_attribute` , `difficulty` )
    VALUES ( NULL ,  'Learning1',  '0',  '1' );"")
    print("Executed raw SQL to create learning skill")
    return

def get_current_db_skills():
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM `dj_sm_00`.`skill_skill` WHERE 1;")
    for row in cursor.fetchone():
        print("Row:", row)
    return row


def create_skill(name='Test skill', pr_attr=0, difficulty=1):
    "" Creates a skill ""
    s = Skill(name=name, primary_attribute=pr_attr, difficulty=difficulty)
    s.save()
    return s


def create_slave(name='Slave', age=1):
    "" Creates a Slave with dayas_delta age ""
    birth_time = timezone.now() - datetime.timedelta(seconds=(GAME_YEAR * age))
    sl = Slave.objects.spawn(name=name, date_birth=birth_time)
#    sl = Slave.objects.spawn()
#    print("create_slave() created slave", sl)
    return sl
"""

class SlaveViewTests(TestCase):
    def test_index_view_with_no_questions(self):

        response = self.client.get(reverse('slave:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No slaves")
        self.assertQuerysetEqual(response.context['slaves_list'], [])

class SlaveDetailTests(TestCase):
    def test_details_view_not_yet_born(self):
        """ View details of Slave with date_init in the future
        should return a 404 """
        future_slave = create_slave("Future Slave", age=-5)
        response = self.client.get(reverse('slave:detail', args=(future_slave.id,)))
        self.assertEqual(response.status_code, 404)
