import os
import re

from flask import Flask

from werkzeug.contrib.fixers import ProxyFix

from changebot.blueprints.stale_issues import stale_issues
from changebot.blueprints.stale_pull_requests import stale_pull_requests
from changebot.blueprints.pull_request_checker import pull_request_checker

app = Flask('astropy-bot')

app.wsgi_app = ProxyFix(app.wsgi_app)

app.integration_id = int(os.environ['GITHUB_APP_INTEGRATION_ID'])
app.private_key = os.environ['GITHUB_APP_PRIVATE_KEY']
app.cron_token = os.environ['CRON_TOKEN']
app.stale_issue_close = os.environ['STALE_ISSUE_CLOSE'].lower() == 'true'
app.stale_issue_close_seconds = float(os.environ['STALE_ISSUE_CLOSE_SECONDS'])
app.stale_issue_warn_seconds = float(os.environ['STALE_ISSUE_WARN_SECONDS'])
app.stale_pull_requests_close = os.environ['STALE_PULL_REQUEST_CLOSE'].lower() == 'true'
app.stale_pull_requests_close_seconds = float(os.environ['STALE_PULL_REQUEST_CLOSE_SECONDS'])
app.stale_pull_requests_warn_seconds = float(os.environ['STALE_PULL_REQUEST_WARN_SECONDS'])


"""
Configuration for the pull request checker.
"""

# This string is formatted with the pr_handler and repo_handler objects
app.pull_request_prolog = re.sub('(\w+)\n', r'\1', """
Thanks for the pull request @{pr_handler.user}!

I am a bot that checks pull requests for milestones and changelog entries.
 If you have any questions about what I am saying, please ask! I
 have the following to report on this pull request:
""").strip() + os.linesep + os.linesep


app.pull_request_epilog = os.linesep + os.linesep + re.sub('(\w+)\n', r'\1', """
*If there are any issues with this message, please report them
 [here](https://github.com/sunpy/sunpy-bot/issues).*
""").strip()

# This should be a substring of either the prolog or the epilog which is used
# to detect previous comments by the bot on the PR
# TODO: Make this automatically determined based on the prolog
app.pull_request_substring = "checks pull requests for"

app.pull_request_passed = 'All checks passed'
app.bot_username = 'sunpy-bot'
app.pull_request_failed = f'There were failures in checks - see comments by @{app.bot_username} above'

# Import this here to register the check with the pull request checker
# from changebot.blueprints.changelog_checker import check_changelog_consistency  # noqa: E402 F401
from changebot.blueprints.milestone_checker import process_milestone  # noqa: E402 F401
from changebot.blueprints.towncrier_changelog_checker import process_towncrier_changelog  # noqa: E402 F401

app.register_blueprint(pull_request_checker)
app.register_blueprint(stale_issues)
app.register_blueprint(stale_pull_requests)


@app.route("/")
def index():
    return "Nothing to see here"


@app.route("/installation_authorized")
def installation_authorized():
    return "Installation authorized"
