from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from slave.models import Slave, Parents
from random import random
from slave.settings import *

class Command(BaseCommand):
    help = "Euthanize the ones ready to die and get new ones born"

    SECONDS_IN_DAY = 86400
    GAME_YEAR = 3600

    def handle(self, *args, **options):
        print("Killer command initiated at:", timezone.now())
        self.killer()
#        self.spawner()
        print("Killer command finished at:", timezone.now())

    def spawner(self):
        males = Slave.objects.all().filter(sex=1, date_death=None)
        females = Slave.objects.all().filter(sex=0, date_death=None)
        print("Before reproduction (males, females):", males.count(), females.count())

        kids = {1:0, 0:0}
        for mom in females:
            if not mom.is_reproductive(): continue
            if len(Slave.objects.filter(parents__parent=mom.id)) >= 2:
#                print(mom, "has 2 kids already")
                if self.flip(len(Slave.objects.filter(parents__parent=mom.id))/10.0):
#                    print(mom, "did not get pregnant this time")
                    continue
            child = Slave.objects.spawn(**{'race': mom.race, 'parents':mom.id})
            kids[child.sex] += 1

        males = Slave.objects.all().filter(sex=1, date_death=None)
        females = Slave.objects.all().filter(sex=0, date_death=None)
        print("After reproduction (males, females):", males.count(), females.count())
        print("During reproduction born (boys, girls):", kids[1], kids[0])

#            child.
#            Parents.objects.create(**{'parent':mom.id})

    
    def killer(self):
        slaves = Slave.objects.filter(date_death=None)
        slaves_count = slaves.count() # We save as we use it later
        print("Before euthanize slaves:", slaves_count)
    
# We split QuerySet to avoid memory leak
        i = 0
        while i <= (slaves_count / KILLER_SLAVES_LIMIT):
            for s in slaves[i:i+KILLER_SLAVES_LIMIT]:
#                print("Check is slave exhausted:", s)
                if self.get_death_risk(s):
                    Slave.objects.kill(s)
            i += 1

        survivors = Slave.objects.all().filter(date_death=None)
        print("After euthanize slaves:", survivors.count())


    def get_death_risk(self, victim):
        """ FIXME Need geometric pdf here """
        age = round((timezone.now() - victim.date_birth).total_seconds() / __class__.GAME_YEAR)
#        print("Victim age is:", age)
#        print("Chance to die:", (age/CHANCE_TO_DIE))
        return True if random() < (age/CHANCE_TO_DIE) else False

    def flip(self, prob):
        return random() < prob



