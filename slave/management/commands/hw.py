from django.core.management.base import BaseCommand, CommandError
from slave.models import Slave

class Command(BaseCommand):
    help = "Returns echo for testing"
    
    def handle(self, *args, **options):
        self.stdout.write("hello world from command")

