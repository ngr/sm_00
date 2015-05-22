from __future__ import absolute_import

from celery import shared_task

from task.models import Task
from slave.models import Slave, Parent
from random import random
from datetime import timedelta
from django.utils import timezone
from django.db.models import F, Count
from slave.settings import *
from slave.helpers import *

@shared_task
def retriever(*args, **options):
    #print("Finding finished tasks")
    ttr = Task.objects.get_finished()
    if len(ttr) < 1:
        #print("No finished Tasks to retrieve")
        return None

    print("Retrieving", ttr)
    for t in ttr:
        try:
            t.retrieve()
        except:
            print("ERROR! Cannot retrieve task {0}.".format(t))

    return "Finished"

@shared_task
def spawner(*args, **options):
    print("Giving birth")
    # Calculate the timespan when the potential mothers were born
    min_age = timezone.now() - timedelta(seconds=(GAME_YEAR * REPRODUCTIVE_AGE))
    max_age = timezone.now() - timedelta(seconds=(GAME_YEAR * END_OF_REPRODUCTIVE_AGE))
    # Get the potential mothers with the current number of kids
    moms = Slave.objects.filter(sex='f', date_death=None, date_birth__lt=min_age, date_birth__gt=max_age).annotate(num_children=Count('children')).values('id', 'name','num_children', 'race', 'location', 'owner')
    print("Reproductive mothers:", moms)
    for m in moms:
        # Get the current chance of birth depending of number of children
        chance_of_birth = fit_to_range_float((CHANCE_OF_REPRODUCTION - (m['num_children'] * CHANCE_OF_REPRODUCTION_DELTA)), minv=0)
        # print("Chance of birth:", chance_of_birth)
        if random() <= chance_of_birth:
            print(m['name'], "got pregnant")
            child = Slave.objects.spawn(race=m['race'], location=m['location'], owner=m['owner'])
            # Saving mother-kid relationship
            # This is a bit zherezzhopu but doesn't create many-to-many other way
            # FIXME one day
            p = Parent.objects.create(date_birth=timezone.now())
            p.child = [child]
            p.parent = [m['id']]
            p.save()

@shared_task
def killer(*args, **options):
    print("Killing slaves at {0}".format(timezone.now()))
    slaves = Slave.objects.filter(date_death=None)
        
    for s in slaves:
        # Index in settings tuple according to sex
        sex = 2 if s.get_sex() == 'm' else 3
        # Chance to die according to settings
        chance = 1.0 / [i[sex] for i in DEATH_RISKS \
            if s.get_age() >= i[0] and s.get_age() <= i[1]][0]
        print("Chance for {0} of age {1}, sex {2} is {3}.".format(s, s.get_age(),s.get_sex(), chance))
        if random() <= chance:
            print("{0} dies".format([s]))
            s.kill()
        
        
        