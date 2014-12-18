from django.test import TestCase

from task.models import Task, RunningTask, Farming
from task.farming import Plant
from skill.models import Skill
from slave.models import Slave

from slave.settings import *

class BasicTaskTests(TestCase):
    def test_create_farming_task(self):
        pass

# Create your tests here.
