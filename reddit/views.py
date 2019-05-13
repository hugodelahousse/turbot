from django.conf import settings
from django.db import transaction
from django.http import HttpResponse
from .utils import reddit
from . import models

from workspaces.utils import get_request_entities, SlackErrorResponse


@transaction.atomic
def subscribe(request):
    team, channel, creator = get_request_entities(request)

    try:
        subreddit = reddit.subreddit(request.POST['text'])
        subreddit.id
    except Exception:
        return SlackErrorResponse(f'Invalid subreddit name: `{request.POST["text"]}`')

    subscription, created = models.Subscription.objects.get_or_create(
        creator=creator,
        channel=channel,
        subreddit=subreddit.display_name,
    )

    if not created:
        return SlackErrorResponse(f'Already subscribed to: `{subreddit.display_name}`')

    settings.SLACK_CLIENT.chat_postMessage(
        channel=channel,
        as_user=False,
        text=f'{creator} added subscription to {subreddit.display_name}'
    )
    return HttpResponse(status=200)


@transaction.atomic
def unsubscribe(request):
    team, channel, creator = get_request_entities(request)
    subreddit = request.POST['text']

    try:
        subscription = models.Subscription.objects.get(
            channel=channel,
            subreddit=subreddit
        )
    except models.Subscription.DoesNotExist:
        return SlackErrorResponse(f'This channel is not subscribed to `{subreddit}`')

    subscription.delete()

    settings.SLACK_CLIENT.chat_postMessage(
        channel=channel,
        as_user=False,
        text=f'{creator} unsubscribed the channel from `{subreddit}`',
    )
    return HttpResponse(200)
