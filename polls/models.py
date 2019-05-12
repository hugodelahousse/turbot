from django.db import models
from django.db.models import CheckConstraint, Q
from django.utils import timezone

from workspaces.models import User, Team, Channel
from workspaces.utils import int_to_emoji


class Poll(models.Model):
    name = models.CharField(max_length=256)
    creator = models.ForeignKey(User, related_name='created_polls', on_delete=models.CASCADE)
    channel = models.ForeignKey(Channel, related_name='polls', on_delete=models.CASCADE)

    @property
    def slack_blocks(self):
        return [
            {
                'type': 'section',
                'text': {
                    'type': 'mrkdwn',
                    'text': f'*{self.name}*',
                },
                'accessory': {
                    'type': 'button',
                    'text': {
                        'type': 'plain_text',
                        'text': 'Delete Poll',
                        'emoji': True
                    },
                    'confirm': {
                        'title': {'type': 'plain_text', 'text': 'Delete Poll'},
                        'text': {'type': 'plain_text', 'text': 'Are you sure you want to delete this poll?'}
                    },
                    'value': 'polls.delete',
                    'action_id': f'{self.id}',
                }
            },
            {
                'type': 'divider'
            },
            *map(lambda c: c.slack_block, self.choices.order_by('index').prefetch_related('voters').all()),
            {
                'type': 'context',
                'elements': [
                    {
                        'type': 'mrkdwn',
                        'text': f'*Created By:* {self.creator.slack_username}',
                    }
                ]
            },
            {
                'type': 'context',
                'elements': [
                    {
                        'type': 'mrkdwn',
                        'text': f'{timezone.now().strftime("Last updated: %x at %H:%M")}',
                    }
                ]
            },
        ]

    def __str__(self):
        return f'Poll {self.name} created by: {self.creator.name} in {self.channel.name}'


class Choice(models.Model):
    index = models.PositiveSmallIntegerField()
    text = models.CharField(max_length=256)
    poll = models.ForeignKey(Poll, related_name='choices', on_delete=models.CASCADE)
    voters = models.ManyToManyField(
        User,
        through='UserChoice',
        through_fields=('choice', 'user'),
        related_name='poll_choices',
    )

    class Meta:
        unique_together = ('index', 'poll')
        constraints = (
            CheckConstraint(check=Q(index__gte=0, index__lt=9), name='index_in_bounds'),
        )

    @property
    def slack_text(self):
        return f'{int_to_emoji(self.index)} {self.text}\t`{self.voters.count()}`'

    @property
    def slack_voters(self):
        return ' '.join(map(lambda u: u.slack_username, self.voters.all()))

    @property
    def slack_block(self):
        return {
            'type': 'section',
            'text': {
                'type': 'mrkdwn',
                'text': f'{self.slack_text}\n{self.slack_voters}'
            },
            'accessory': {
                'type': 'button',
                'text': {
                    'type': 'plain_text',
                    'text': 'Vote',
                    'emoji': True,
                },
                'action_id': f'{self.id}',
                'value': 'polls.vote',
            }
        }

    def __str__(self):
        return f'Choice "{self.text}" of poll "{self.poll.name}" ({self.poll.id})'


class UserChoice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'choice')
        ordering = ('created_at', )
