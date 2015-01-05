from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from slave.models import Slave, Parents
from slave.tasks import retriever
from random import random
from slave.settings import *

class Command(BaseCommand):
    help = "call delayed tasks to Celery queue"


    def handle(self, *args, **options):
        retriever.delay()

