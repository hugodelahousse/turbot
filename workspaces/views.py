import logging
import requests

import ujson as json
from django.http import HttpResponse, JsonResponse
from slack import WebClient

from acu_bot import settings
from workspaces.models import User
from workspaces.utils import SLACK_ACTIONS, register_slack_action

sc = WebClient(settings.SLACK_API_TOKEN)
logger = logging.getLogger('django')


def get_photo_blocks(login, url, stalker=None):
    blocks = [
        {'type': 'section', 'text': {'type': 'mrkdwn', 'text': f'*{login}*'}},
        {'type': 'image', 'title': {'type': 'plain_text', 'text': f'{login}'}, 'image_url': url,
         'alt_text': f'{login}'},

    ]
    if not stalker:
        blocks.append({
            'type': 'actions',
            'elements': [
                {
                    'type': 'button', 'text': {'type': 'plain_text', 'text': 'Send to Channel', },
                    'action_id': login, 'value': 'photo.post',
                }
            ]
        })

    if stalker:
        blocks.append(
            {'type': 'context', 'elements': [{'type': 'mrkdwn', 'text': f'*Stalké Par: {stalker.slack_username}*'}]})

    return blocks


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

    return JsonResponse({
        'text': f'CRI Picture of {login}',
        'blocks': get_photo_blocks(login, response.url)
    })


@register_slack_action('photo.post')
def post_photo(payload):
    stalker = User(payload['user']['id'])
    login = payload['actions'][0]['action_id']

    blocks = get_photo_blocks(
            login,
            f'https://photos.cri.epita.fr/thumb/{login}',
            stalker
    )

    logger.debug(blocks)

    logger.debug(sc.chat_postMessage(
        text=f'CRI Picture of {login}',
        channel=payload['channel']['id'],
        blocks=blocks,
        as_user=False,
    ))
    return HttpResponse(200)
