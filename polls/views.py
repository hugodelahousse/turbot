import logging
import re

from django.db import transaction
from django.http import HttpResponse

from polls.models import Poll, Choice
from workspaces.models import User
from workspaces.utils import SlackErrorResponse, get_request_entities, register_slack_action
from slackclient import SlackClient
from django.conf import settings

sc = SlackClient(settings.SLACK_API_TOKEN)
logger = logging.getLogger('django')


@transaction.atomic
@register_slack_action('polls.vote')
def vote(payload):
    user, _ = User.objects.get_or_create(id=payload['user']['id'], team_id=payload['user']['team_id'], defaults={
        'name': payload['user']['username']
    })

    choice = Choice.objects.prefetch_related('voters').get(id=payload['actions'][0]['action_id'])

    if choice.voters.filter(id=user.id).exists():
        choice.voters.remove(user)
    else:
        choice.voters.add(user)

    logger.debug(sc.api_call(
        'chat.update', ts=payload['message']['ts'], text='',
        channel=payload['channel']['id'], as_user=False,
        blocks=choice.poll.slack_blocks
    ))

    return HttpResponse(status=200)


@transaction.atomic
@register_slack_action('polls.delete')
def delete(payload):
    user = User.objects.get(id=payload['user']['id'])
    poll = Poll.objects.get(id=payload['actions'][0]['action_id'])

    logger.debug(sc.api_call(
        'chat.delete',
        ts=payload['message']['ts'],
        channel=poll.channel.id,
        as_user=False,
    ))

    logger.debug(sc.api_call(
        'chat.postMessage',
        text=f'A poll was deleted by {user.slack_username}',
        channel=poll.channel.id,
        as_user=False
    ))

    poll.delete()
    return HttpResponse(status=200)


@transaction.atomic
def create(request):
    values = re.findall(r'\s*"([^"]+)"\s*', request.POST['text'])
    if len(values) < 3:
        return SlackErrorResponse(':x: You must provide a name and at least two choices :x:')
    name, *choices = values
    if len(choices) > 9:
        return SlackErrorResponse(':x: You cannot have more than 9 choices :x:')

    team, channel, creator = get_request_entities(request)

    poll = Poll.objects.create(
        name=name,
        creator=creator,
        channel=channel,
    )

    for index, choice in enumerate(choices):
        poll.choices.create(index=index, text=choice)

    logger.debug(sc.api_call(
        'chat.postMessage',
        channel=channel.id,
        text='',
        blocks=poll.slack_blocks,
        as_user=False
    ))

    return HttpResponse(status=200)
