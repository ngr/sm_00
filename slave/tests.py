from django.test import TestCase
from django.utils import timezone
from django.core.urlresolvers import reverse
import datetime
from random import random

from slave.models import Slave, SlaveManager, RaceDefaults


class SlaveManagerTests(TestCase):
    attribs = ['strength', 'intelligence', 'agility', 'charisma']
    
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
        self.assertEqual(Slave.objects.all().filter(name=test_name)[0].is_alive(), True)

    def test_kill_update_in_db(self):
        """ Checks if kill() sets the date_death to now() """
        create_slave()
        Slave.objects.kill(Slave.objects.latest('date_birth'))
        victim = Slave.objects.latest('date_birth')
        self.assertIsNotNone(victim.date_death)

    def test_kill_with_date_specified(self):
        create_slave()
        kill_date = timezone.now().replace(microsecond=0) - datetime.timedelta(days=3)
        print(kill_date)
        Slave.objects.kill(Slave.objects.latest('date_birth'), kill_date)
        victim = Slave.objects.latest('date_birth')
        self.assertEqual(victim.date_death, kill_date)


class SlaveMethodTests(TestCase):
    def test_is_child_with_not_yet_born(self):
        """ List of slaves should not show objects
        with date_init in the future """
        time = timezone.now() + datetime.timedelta(hours=1)
        future_slave = Slave(date_birth=time)
        self.assertEqual(future_slave.is_child(), False)

    def test_is_child_with_old_slave(self):
        time = timezone.now() - datetime.timedelta(days=10)
        old_slave = Slave(date_birth=time)
        self.assertEqual(old_slave.is_child(), False)

    def test_is_child_with_child_slave(self):
        time = timezone.now() - datetime.timedelta(hours=1)
        child_slave = Slave(date_birth=time)
        self.assertEqual(child_slave.is_child(), True)

    def test_is_alive_with_not_yet_born(self):
        time = timezone.now() + datetime.timedelta(hours=1)
        future_slave = Slave(date_birth=time)
        self.assertEqual(future_slave.is_alive(), False)

    def test_is_alive_with_already_dead(self):
        time = timezone.now()
        birth_time = timezone.now() - datetime.timedelta(days=21)
        future_slave = Slave(date_birth=birth_time, date_death=time)
        self.assertEqual(future_slave.is_alive(), False)


class RaceDefaultsTests(TestCase):
    def test_is_attribute_in_range(self):
        attribs = ['strength', 'intelligence', 'agility', 'charisma']
        for a in attribs:
            for param in RaceDefaults.objects.all().filter(param=a):
                self.assertIn(param.value, range(1,11))


def create_slave(name='Slave', age=1):
    """ Creates a Slave with dayas_delta age """
    birth_time = timezone.now() - datetime.timedelta(days=age)
    return Slave.objects.create(name=name, date_birth=birth_time)

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
