from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from slave.models import Slave
from random import random

class Command(BaseCommand):
    help = "Kill the ones ready to die"

    SECONDS_IN_DAY = 86400

    def handle(self, *args, **options):
        self.killer()
        self.spawner()

    def spawner(self):
        females = Slave.objects.all().filter(sex=1, date_death=None)
        print(females.count())
        for mom in females:
            if not mom.is_adult(): continue
            Slave.objects.spawn(**{'race': mom.race})

    
    def killer(self):
        slaves = Slave.objects.all().filter(date_death=None)
        for s in slaves:
#            print("Check is slave exhausted:", s)
            if self.get_death_risk(s):
                Slave.objects.kill(s)

    def get_death_risk(self, victim):
        """ FIXME Need geometric pdf here """
        age = round((timezone.now() - victim.date_birth).total_seconds() / __class__.SECONDS_IN_DAY)
#       print("Victim age is:", age)
#       print("Chance to die:", (age/1000.0))
        return True if random() < (age/1000.0) else False

    



