from django.core.management.base import BaseCommand
from django.utils import timezone

class Command(BaseCommand):
    help = 'say hello'

    def handle(self, *args, **kwargs):
        print("hello world")
        time = timezone.now().strftime('%X')
        print("It's now %s" % time)