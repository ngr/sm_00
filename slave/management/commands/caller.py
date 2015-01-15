from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from slave.models import Slave, Parents
from slave.tasks import retriever, food_expire, wh_cleaner
from random import random
from slave.settings import *

class Command(BaseCommand):
    help = "call delayed tasks to Celery queue"


    def handle(self, *args, **options):
        retriever.delay()
        food_expire.delay()
        wh_cleaner.delay()


