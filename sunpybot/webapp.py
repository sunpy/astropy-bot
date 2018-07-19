import os

from flask import Flask

from werkzeug.contrib.fixers import ProxyFix

from baldrick.blueprints import github, circleci

"""
Configure the App
"""

app = Flask('sunpy-bot')

app.wsgi_app = ProxyFix(app.wsgi_app)

app.integration_id = int(os.environ['GITHUB_APP_INTEGRATION_ID'])
app.private_key = os.environ['GITHUB_APP_PRIVATE_KEY']

app.bot_username = 'sunpy-bot'

app.register_blueprint(github)
app.register_blueprint(circleci)


"""
Configure Plugins
"""

# Register the circleci artifact checker
import baldrick.plugins.artifact_checker  # noqa
import baldrick.plugins.milestone_checker  # noqa
import baldrick.plugins.towncrier_changelog_checker  # noqa


@app.route("/")
def index():
    return "Nothing to see here"


@app.route("/installation_authorized")
def installation_authorized():
    return "Installation authorized"
