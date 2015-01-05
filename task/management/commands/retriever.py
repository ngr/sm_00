from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
#from slave.models import Slave
from task.models import Task, Assignment
from random import random
from slave.settings import *

class Command(BaseCommand):
    help = "Retrieve finished tasks"

    @shared_task
    def handle(self, *args, **options):
        print("Finding finished tasks")
        # ttr - Tasks To Retrieve
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

        print("Finished")





