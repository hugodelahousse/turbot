from django.core.management.base import BaseCommand, CommandError
from reddit.utils import trigger_submissions


class Command(BaseCommand):
    help = 'Sends posts to channels with subscriptions'

    def handle(self, *args, **options):
        trigger_submissions()
