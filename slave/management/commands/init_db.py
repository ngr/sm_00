from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from slave.models import Slave
import datetime
import random

class Command(BaseCommand):
    help = "Refill slaves DB after Truncate"

    SECONDS_IN_DAY = 3600

    def handle(self, *args, **options):
#        self.killer()
        self.spawner()

    def spawner(self):
        for i in range(5000):
            date_birth = timezone.now() - datetime.timedelta(hours=random.randrange(0,75))
            s = Slave.objects.spawn(**{'date_birth': date_birth})


