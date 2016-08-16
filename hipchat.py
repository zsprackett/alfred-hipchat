# encoding: utf-8

import sys
import argparse
import re
import json
from urllib2 import URLError
import webbrowser
import requests
from workflow import Workflow, web, PasswordNotFound

def hipchat_keys():
    wflw = Workflow()
    try:
        keys = wflw.get_password('hipchat_api_key')
    except PasswordNotFound:
        wflw.add_item(title='No API key set. Please run hipchat_api_token', valid=False)
        wflw.send_feedback()
        return 0
    return keys.split(",")

def hipchat_list(keys):
    wflw = Workflow()
    hipchat_search = []

    for key in keys:
        api_key = str(key)
        try:
            hipchat_auth = web.get('https://api.hipchat.com/v2/room?auth_token=' +
                                   api_key + '&auth_test=true',
                                   None,
                                   timeout=wflw.settings['timeout'])
        except URLError, requests.SSLError:
            wflw.add_item(title='Error connecting to HipChat API.',
                          valid=False)
            wflw.send_feedback()
            return None

        if not hipchat_auth or \
           not hipchat_auth.status_code == requests.codes.accepted or \
           not 'success' in hipchat_auth.json():

            wflw.add_item(title='Authentication failed. Check your API token',
                          valid=False)
            wflw.send_feedback()
            return None
        else:
            try:
                hipchat_rooms = web.get(wflw.settings['api_url'] +
                                        '/v2/room?auth_token=' +
                                        api_key + '&max-results=1000',
                                        None,
                                        timeout=wflw.settings['timeout']
                                       ).json()
                hipchat_users = web.get(wflw.settings['api_url'] +
                                        '/v2/user?auth_token=' +
                                        api_key + '&max-results=1000',
                                        None,
                                        timeout=wflw.settings['timeout']
                                       ).json()
            except URLError, requests.SSLError:
                wflw.add_item(title='Error fetching lists from HipChat API.',
                              valid=False)
                wflw.send_feedback()
                return None

            for room in hipchat_rooms['items']:
                hipchat_search.append({
                    'name': room['name'],
                    'id': room['id'],
                    'description': "%s Room" % room['privacy'].title(),
                    'type': 'room'
                    })
            for user in hipchat_users['items']:
                hipchat_search.append({
                    'name': user['name'],
                    'mention_name': user['mention_name'],
                    'id': user['id'],
                    'description': "User @%s" % user['mention_name'],
                    'type': "user"})
    return hipchat_search

def search_hipchat_names(hlist):
    elements = []
    elements.append(hlist['name'])
    if hlist['type'] == "user":
        elements.append(u'@' + hlist['mention_name'])
    return u' '.join(elements)

def hipchat_urlopen(target_json):
    url = ""
    try:
        wflw = Workflow()
        tgt = json.loads(target_json)
        url = "hipchat://%s/%s/%s" % (wflw.settings['hipchat_host'],
                                      tgt['type'], tgt['id'])
    except ValueError:
        pass
    return url

def main(wflw):
    parser = argparse.ArgumentParser()
    parser.add_argument('--api_key', dest='api_key', nargs='?', default=None)
    parser.add_argument('--api_url', dest='api_url', nargs='?', default=None)
    parser.add_argument('--cache_max_age', dest='cache_max_age', nargs='?', default=None)
    parser.add_argument('--hipchat_host', dest='hipchat_host', nargs='?', default=None)
    parser.add_argument('--open', dest='open', nargs='?')
    parser.add_argument('query', nargs='?', default=None)
    args = parser.parse_args(wflw.args)

    if args.api_key:
        wflw.save_password('hipchat_api_key', args.api_key)
        return

    if args.hipchat_host:
        WF.settings['hipchat_host'] = re.sub(r"(^https?://)",
                                             "", args.hipchat_host)
        return

    if args.api_url:
        WF.settings['api_url'] = args.api_url
        return

    if args.cache_max_age:
        WF.settings['cache_max_age'] = args.cache_max_age
        return

    # settings go above here
    if 'hipchat_host' not in WF.settings:
        wflw.add_item(title='HipChat hostname is not set.  Please run hipchat_hostname <url>',
                      valid=False)
        wflw.send_feedback()
        return None

    if args.open:
        url = hipchat_urlopen(wflw.args[1])
        webbrowser.open(url)
        return

    if len(wflw.args):
        query = wflw.args[0]
    else:
        query = None

    def wrapper():
        return hipchat_list(keys=hipchat_keys())

    hipchat_search = wflw.cached_data('alfred-hipchat',
                                      wrapper,
                                      max_age=wflw.settings['cache_max_age'])

    if query:
        hipchat_search = wflw.filter(query,
                                     hipchat_search,
                                     key=search_hipchat_names,
                                     min_score=20)

    if hipchat_search:
        for item in hipchat_search:
            wflw.add_item(
                title=item['name'],
                subtitle=item['description'],
                arg=json.dumps(item),
                valid=True
                )
        wflw.send_feedback()


if __name__ == u"__main__":
    WF = Workflow()
    if 'api_url' not in WF.settings:
        WF.settings['api_url'] = "https://api.hipchat.com"
    if 'timeout' not in WF.settings:
        WF.settings['timeout'] = 5
    if 'cache_max_age' not in WF.settings:
        WF.settings['cache_max_age'] = 180
    sys.exit(WF.run(main))
