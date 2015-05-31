from django.core.management.base import BaseCommand, CommandError
from slave.tasks import killer

class Command(BaseCommand):
    help = "Call kill some slaves task to Celery queue"

    def handle(self, *args, **options):
        killer.delay()