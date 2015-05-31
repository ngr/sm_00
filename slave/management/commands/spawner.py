from django.core.management.base import BaseCommand, CommandError
from slave.tasks import spawner

class Command(BaseCommand):
    help = "Call spawn new slaves task to Celery queue"

    def handle(self, *args, **options):
        spawner.delay()