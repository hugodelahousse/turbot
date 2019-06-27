from django.test import TestCase
from .views import get_poll_choices, InvalidPollException


class TestPollChoices(TestCase):
    def test_base_case(self):
        name, choices = get_poll_choices(r'"Simple Question" "Answer 1" "Answer 2"')
        self.assertEqual("Simple Question", name)
        self.assertEqual(["Answer 1", "Answer 2"], choices)

    def test_raises_too_few(self):
        with self.assertRaisesMessage(
            InvalidPollException, "You must provide a name and at least two choices"
        ):
            name, choices = get_poll_choices('"Simple Question" "Answer 1"')

    def test_raises_too_many(self):
        with self.assertRaisesMessage(
            InvalidPollException, "You cannot have more than 9 choices"
        ):
            name, choices = get_poll_choices(
                '"Simple Question" "1" "2" "3" "4" "5" "6" "7" "8" "9" "10"'
            )

    def test_custom_quotes(self):
        name, choices = get_poll_choices(r'"Simple Question" "1" "2" “3” ‘4’ “5"')
        self.assertEqual("Simple Question", name)
        self.assertEqual(["1", "2", "3", "4", "5"], choices)
