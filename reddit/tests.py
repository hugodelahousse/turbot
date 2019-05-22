from unittest.mock import patch, MagicMock
import slack

from django.test import TestCase
import datetime

from model_mommy import mommy

from reddit.utils import trigger_submissions
from django.conf import settings

NOW = datetime.datetime.now()


def fixed_datetime(**kwargs):
    class Datetime(datetime.datetime):
        @staticmethod
        def now():
            return NOW.replace(**kwargs)

    return Datetime


class TestTrigger(TestCase):
    slack_client = None

    def setUp(self):
        self.slack_client = MagicMock(slack.WebClient)

    @patch("datetime.datetime", fixed_datetime(hour=settings.NIGHT_END.hour - 1))
    def test_nighttime(self):
        with self.settings(SLACK_CLIENT=self.slack_client):
            trigger_submissions()
            self.slack_client.chat_postMessage.assert_not_called()

    @patch("datetime.datetime", fixed_datetime(hour=settings.NIGHT_END.hour + 1))
    def test_trigger(self):
        mommy.make("reddit.Subscription", subreddit="aww")

        with self.settings(SLACK_CLIENT=self.slack_client):
            trigger_submissions()
            self.slack_client.chat_postMessage.assert_called_once()
