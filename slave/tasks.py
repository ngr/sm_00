from __future__ import absolute_import

from celery import shared_task

from task.models import Task, Assignment
from item.models import Item, ItemDirectory, FoodDirectory, ItemJoffreyList
from random import random
from datetime import timedelta
from django.utils import timezone
from slave.settings import *

@shared_task
def retriever(*args, **options):
    print("Finding finished tasks")
    ttr = Task.objects.get_finished()
    if len(ttr) < 1:
        print("No finished Tasks to retrieve")
        return None

    print("Retrieving", ttr)
    for t in ttr:
        try:
            t.retrieve()
        except TaskError:
            print("ERROR! Cannot retrieve task {0}.".format(t))

    return "Finished"

@ shared_task
def food_expire(*args, **kwargs):
    print("Calculating food expiration")
    f = Item.objects.filter(itemjoffreylist__isnull=True, _itype___related__fooddirectory__isnull=False).all()

    print("Analysing items not yet in JoffreyList", f)

    n = timezone.now()
# Way #1. Calculate for every item.
    for i in f:
        std_exp_time = i.get_date_init() + timedelta(seconds=(MIN_FOOD_SHELF_LIFE\
            * i._itype._related.filter(fooddirectory__isnull=False).last().fooddirectory._shelf_life))
        print("Standard expiry time for {0} is {1} seconds".format(i, std_exp_time))

        jl = ItemJoffreyList(item=i,
                execution_time=std_exp_time,
                reason="Set by foodexp at {0}".format(n))
        jl.save()


@shared_task
def wh_cleaner(*args, **kwargs):
    """ Clean Item objects no longer used by any game objects.
        This uses pure SQL delete, so the custom destroy() method 
        is not called for performance bonus. """

    print("Cleaning zero amount items")
    Item.objects.filter(_amount=0).delete()

    print("Destroying expired food")
    n = timezone.now()
    Item.objects.filter(itemjoffreylist__execution_time__lt=n).delete()
    ItemJoffreyList.objects.filter(execution_time__lt=n).delete()
    



