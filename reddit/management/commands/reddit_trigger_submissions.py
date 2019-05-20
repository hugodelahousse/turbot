from django.core.management.base import BaseCommand, CommandError
from reddit.utils import trigger_submissions


class Command(BaseCommand):
    help = "Sends posts to channels with subscriptions"

    def add_arguments(self, parser):
        parser.add_argument("channels", nargs="*", type=str)

    def handle(self, *args, **options):
        trigger_submissions(*options["channels"])
