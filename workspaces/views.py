import ujson as json
from workspaces.utils import SLACK_ACTIONS


def oauth(request):

    return 'ok'


def test(request):
    print(request.body)
    return 'ok'


def action(request):
    payload = json.loads(request.POST['payload'])
    action_name: str = payload['actions'][0]['value']
    return SLACK_ACTIONS[action_name](payload)

