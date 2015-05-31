from django.core.management.base import BaseCommand, CommandError
from slave.tasks import retriever

class Command(BaseCommand):
    help = "call delayed tasks to Celery queue"

    def handle(self, *args, **options):
        retriever.delay()
        