from django.test import TestCase
from django.utils import timezone
from django.core.urlresolvers import reverse
import datetime

from slave.models import Slave

class SlaveMethodTests(TestCase):

    def test_is_child_with_not_yet_born(self):
        """ List of slaves should not show objects
        with date_init in the future """
        time = timezone.now() + datetime.timedelta(days=10)
        future_slave = Slave(date_init=time)
        self.assertEqual(future_slave.is_child(), False)

    def test_is_child_with_old_slave(self):
        time = timezone.now() - datetime.timedelta(days=10)
        old_slave = Slave(date_init=time)
        self.assertEqual(old_slave.is_child(), False)

    def test_is_child_with_child_slave(self):
        time = timezone.now() - datetime.timedelta(hours=1)
        child_slave = Slave(date_init=time)
        self.assertEqual(child_slave.is_child(), True)

def create_slave(name, age):
    """ Creates a Slave with dayas_delta age """
    birth_date = timezone.now() - datetime.timedelta(days=age)
    return Slave.objects.create(name=name, date_init=birth_date)

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
