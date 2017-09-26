import os
import time
import requests

URL = "https://astrochangebot.herokuapp.com"

TOKEN = os.environ['CRON_TOKEN']
INSTALLATION = os.environ['INSTALLATION_ID']

repositories = ['astropy-helpers']

for hook in ['/close_stale_issues', '/close_stale_pull_requests']:

    for repository in repositories:

        print(f'Triggering {hook} for repository {repository}')

        data = {'repository': repository,
                'cron_token': TOKEN,
                'installation': INSTALLATION}

        requests.post(URL, json=data)

        time.sleep(10)
