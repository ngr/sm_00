from __future__ import absolute_import

from celery import shared_task

from task.models import Task, Assignment
from random import random
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




