from typing import Tuple

from django.http import JsonResponse, HttpRequest
from django.conf import settings

from workspaces.models import Team, Channel, User
import logging

SLACK_ACTIONS = {}

logger = logging.getLogger('django')


def register_slack_action(name):
    def __inner(f):
        SLACK_ACTIONS[name] = f
        return f

    return __inner


class SlackErrorResponse(JsonResponse):
    def __init__(self, text: str, *args, **kwargs):
        super().__init__({
            'response_type': 'ephemeral',
            'text': text,
            'icon_url': settings.ERROR_ICON_URL,
        }, *args, **kwargs)


def int_to_emoji(index: int):
    return [':one:', ':two:', ':three:', ':four:', ':five:', ':six:', ':seven:', ':eight:', ':nine:'][index]


def get_request_entities(request: HttpRequest) -> Tuple[Team, Channel, User]:
    logger.debug(request.POST)
    team, _ = Team.objects.get_or_create(
        id=request.POST['team_id'],
        defaults={'domain': request.POST['team_domain']}
    )

    channel, _ = Channel.objects.get_or_create(
        id=request.POST['channel_id'],
        team=team,
        defaults={'name': request.POST['channel_name']}
    )

    user, _ = User.objects.get_or_create(
        id=request.POST['user_id'],
        team=team,
        defaults={
            'name': request.POST['user_name']
        }
    )

    return team, channel, user
