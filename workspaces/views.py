import logging
import requests

import ujson as json
from django.http import HttpResponse, JsonResponse

from turbot import settings
from workspaces.models import User
from workspaces.utils import SLACK_ACTIONS, register_slack_action

logger = logging.getLogger("django")


def get_photo_blocks(photo_slug, url, stalker=None):
    blocks = [
        {"type": "section", "text": {"type": "mrkdwn", "text": f"*{photo_slug}*"}},
        {
            "type": "image",
            "title": {"type": "plain_text", "text": f"{photo_slug}"},
            "image_url": url,
            "alt_text": f"{photo_slug}",
        },
    ]
    if not stalker:
        blocks.append(
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {"type": "plain_text", "text": "Send to Channel"},
                        "action_id": photo_slug,
                        "value": "photo.post",
                    }
                ],
            }
        )

    if stalker:
        blocks.append(
            {
                "type": "context",
                "elements": [
                    {
                        "type": "mrkdwn",
                        "text": f"*Stalké Par: {stalker.slack_username}*",
                    }
                ],
            }
        )

    return blocks


def oauth(request):
    return "ok"


def test(request):
    return "ok"


def action(request):
    payload = json.loads(request.POST["payload"])
    logger.debug(payload)
    action_name: str = payload["actions"][0]["value"]
    return SLACK_ACTIONS[action_name](payload)


def photo(request):
    photo_slug = request.POST["text"]
    response = requests.head(settings.PHOTO_FSTRING.format(photo_slug))
    if response.status_code != 200:
        return HttpResponse("No such photo_slug")

    return JsonResponse(
        {
            "text": f"Picture of {photo_slug}",
            "blocks": get_photo_blocks(photo_slug, response.url),
        }
    )


@register_slack_action("photo.post")
def post_photo(payload):
    stalker = User(payload["user"]["id"])
    photo_slug = payload["actions"][0]["action_id"]

    blocks = get_photo_blocks(
        photo_slug, settings.PHOTO_FSTRING.format(photo_slug), stalker
    )

    logger.debug(blocks)

    logger.debug(
        settings.SLACK_CLIENT.chat_postMessage(
            text=f"Picture of {photo_slug}",
            channel=payload["channel"]["id"],
            blocks=blocks,
            as_user=False,
        )
    )
    return HttpResponse(200)
