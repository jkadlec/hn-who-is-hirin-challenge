import requests
from collections import deque


def _get_session():
    req = requests.get('http://challenge.shopcurbside.com/get-session')
    return req.text


def _dfs(seed_next, session):
    next_links = deque(seed_next)
    secret = ''
    while any(next_links):
        curr = next_links.pop()
        req = requests.get('http://challenge.shopcurbside.com/%s' % curr, headers={'Session':session})
        if req.status_code == 404:
            session = _get_session()
            next_links.append(curr)
            continue

        if 'secret' in req.json():
            secret = req.json()['secret'] + secret
        json_reply = req.json()
        json_reply = {k.lower():v for k, v in json_reply.items()}
        if not 'next' in json_reply:
            continue

        next_req = json_reply['next']
        if isinstance(next_req, list):
            next_links.extend(next_req)
        else:
            next_links.append(next_req)

    return secret
    

start_uri = 'http://challenge.shopcurbside.com/start'

session = _get_session()
req = requests.get(start_uri, headers={'Session':session})
print(_dfs((req.json()['next']), session))


