import logging
import requests

import ujson as json
from django.http import HttpResponse, JsonResponse

from workspaces.models import User
from workspaces.utils import SLACK_ACTIONS

logger = logging.getLogger('django')


def oauth(request):
    return 'ok'


def test(request):
    return 'ok'


def action(request):
    payload = json.loads(request.POST['payload'])
    logger.debug(payload)
    action_name: str = payload['actions'][0]['value']
    return SLACK_ACTIONS[action_name](payload)


def photo(request):
    login = request.POST['text']
    response = requests.head(f'https://photos.cri.epita.fr/thumb/{login}')
    if response.status_code != 200:
        return HttpResponse('No such login')

    stalker = User(id=request.POST['user_id'])

    return JsonResponse({
        'text': '',
        'blocks': [
            {
                'type': 'section',
                'text': {
                    'type': 'mrkdwn',
                    'text': f'*{login}*'
                }
            },
            {
                'type': 'image',
                'title': {
                    'type': 'plain_text',
                    'text': f'{login}',
                },
                'image_url': response.url,
                'alt_text': f'{login}'
            },
            {
                'type': 'context',
                'elements': [
                    {
                        'type': 'mrkdwn',
                        'text': f'*Stalké Par: {stalker.slack_username}*'
                    }
                ]
            }
        ]
    })
