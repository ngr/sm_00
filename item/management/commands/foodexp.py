from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from slave.models import Slave, Parents
from item.models import Item, ItemJoffreyList
from slave.tasks import retriever
from random import random
from datetime import timedelta
from slave.settings import *

class Command(BaseCommand):
    help = "Calculate food expiration"


    def handle(self, *args, **options):
        print("Calculating food expiration")
        f = Item.objects.filter(itemjoffreylist__isnull=True, _itype___related__fooddirectory__isnull=False).all()

        print("Analysing items not yet in JoffreyList", f)

        n = timezone.now()
# Way #1. Calculate for every item.
        for i in f:
            std_exp_time = MIN_FOOD_SHELF_LIFE\
                * i._itype._related.filter(fooddirectory__isnull=False).last().fooddirectory._shelf_life
            print("Standard expiry time for {0} is {1} seconds".format(i, std_exp_time))

            jl = ItemJoffreyList(item=i, 
                    execution_time=(n + timedelta(seconds=std_exp_time)),
                    reason="Set by foodexp at {0}".format(n))
            jl.save()

# Way #2. Prefetch standard expiry times for different Plants.


