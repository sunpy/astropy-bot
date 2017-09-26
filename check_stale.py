import os
import time
import requests

URL = "https://astrochangebot.herokuapp.com"

TOKEN = os.environ['CRON_TOKEN']
INSTALLATION = os.environ['INSTALLATION_ID']

repositories = ['astropy/astropy', 'astropy/astropy-helpers']

for hook in ['/close_stale_issues', '/close_stale_pull_requests']:

    for repository in repositories:

        print(f'Triggering {hook} for repository {repository}')

        data = {'repository': repository,
                'cron_token': TOKEN,
                'installation': INSTALLATION}

        req = requests.post(URL + hook, json=data)
        print(req.content)
        assert req.ok

        time.sleep(10)
