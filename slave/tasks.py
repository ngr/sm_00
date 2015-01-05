from __future__ import absolute_import

from celery import shared_task

from task.models import Task, Assignment
from random import random
from slave.settings import *

@shared_task
def retriever(param=None):
    print("Finding finished tasks")
    ttr = Task.objects.get_finished()
    if len(ttr) < 1:
        print("No finished Tasks to retrieve")
        return None

    print("Retrieving", ttr)
    for t in ttr:
        t.retrieve()

    return "Finished"

