from django.core.management.base import BaseCommand, CommandError
#from django.utils import timezone
#from slave.models import Slave, Parents
from slave.tasks import wh_cleaner, retriever
#from random import random
#from slave.settings import *

class Command(BaseCommand):
    help = "Clean garbage"

    def handle(self, *args, **options):
        wh_cleaner()

