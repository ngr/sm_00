from django.test import TestCase

from task.models import Task, RunningTask, Farming
from task.farming import Plant
from skill.models import Skill
from slave.models import Slave

from slave.settings import *
from slave.helpers_test import *

class BasicTaskTests(TestCase):

    def _prepare_farming(self):
        self.sl = create_slave()
        self.sk1 = create_skill()
        self.sk2 = create_skill()

        p = make_plant()

    def _create_farming_task(self):
        sl = create_slave()
        sk = create_skill()
        train_skill(sl, sk)

        p = make_plant()
        t = Farming.objects.assign(sl, p)
        return t

    def test_create_farming_task(self):
        t = self._create_farming_task()
        self.assertEqual(t.__class__.__name__, 'Farming')


    def test_farming_yield_with_zero_skills(self):
        """ Yield should return zero result in case of 
            neither primary nor secondary skills trained """

        t = self._create_farming_task()
        self.assertEqual(t.retrieve(), 0)


# Create your tests here.
